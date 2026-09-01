import json
import re
from typing import Dict

from backend.llm.gemini_provider import GeminiProvider


ROUTING_SYSTEM_PROMPT = """
You are the intent router for ShopAssist AI.

Classify the customer's request into exactly ONE of these intents:

order_support
shipping
returns
refunds
cancellations
payments
account_support
product_information
general_support

Return ONLY a JSON object. Do not use markdown. Do not explain your answer.

Required format:
{"intent":"order_support","confidence":0.95}

Intent definitions:

order_support:
Questions about an existing order, order status, order number, processing,
shipped status, delivered status, or where an order currently is.

shipping:
Questions about shipping methods, delivery time, estimated delivery,
tracking, shipping delays, or delivery information.

returns:
Questions about returning a product, return eligibility, return policy,
or how to initiate a return.

refunds:
Questions about refunds, refund status, refund processing time, or a
refund that has not appeared.

cancellations:
Questions specifically asking to cancel an order.

payments:
Questions about failed payments, payment methods, cards, billing,
or payment problems.

account_support:
Questions about passwords, login, account access, or compromised accounts.

product_information:
Questions about product availability, specifications, dimensions,
compatibility, features, or included accessories.

general_support:
Questions that do not clearly belong to one of the categories above.

Important distinctions:
- "Where is my order?" = order_support
- "What is the delivery time?" = shipping
- "Can I return this?" = returns
- "Where is my refund?" = refunds
- "Can I cancel my order?" = cancellations
- "My payment failed." = payments
- "I forgot my password." = account_support
- "Is this compatible with my device?" = product_information

Confidence must be a number between 0 and 1.
"""


ALLOWED_INTENTS = {
    "order_support",
    "shipping",
    "returns",
    "refunds",
    "cancellations",
    "payments",
    "account_support",
    "product_information",
    "general_support",
}


class IntentRouter:
    """
    Hybrid intent router.

    Gemini is the primary classifier.
    A deterministic fallback is used when Gemini is unavailable,
    rate-limited, or returns malformed output.
    """

    def __init__(self):
        self.provider = GeminiProvider()

    def route(self, message: str) -> Dict:
        try:
            response = self.provider.generate(
                system_prompt=ROUTING_SYSTEM_PROMPT,
                user_prompt=message,
            )

            raw_answer = str(
                response.get("answer", "")
            ).strip()

            parsed = self._parse_json(raw_answer)

            intent = parsed.get("intent")
            confidence = parsed.get("confidence")

            if intent in ALLOWED_INTENTS:
                try:
                    confidence = float(confidence)
                except (TypeError, ValueError):
                    confidence = 0.8

                confidence = max(
                    0.0,
                    min(1.0, confidence),
                )

                return {
                    "intent": intent,
                    "confidence": confidence,
                    "routing_method": "gemini",
                }

        except Exception as exc:
            print(
                f"Gemini routing unavailable; "
                f"using deterministic fallback: "
                f"{type(exc).__name__}: {exc}"
            )

        fallback_intent, fallback_confidence = (
            self._fallback_classify(message)
        )

        return {
            "intent": fallback_intent,
            "confidence": fallback_confidence,
            "routing_method": "deterministic_fallback",
        }

    @staticmethod
    def _parse_json(text: str) -> Dict:
        if not text:
            return {}

        text = text.strip()

        try:
            parsed = json.loads(text)
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            pass

        match = re.search(
            r"```(?:json)?\s*(\{.*?\})\s*```",
            text,
            re.DOTALL | re.IGNORECASE,
        )

        if match:
            try:
                parsed = json.loads(match.group(1))
                return parsed if isinstance(parsed, dict) else {}
            except json.JSONDecodeError:
                pass

        match = re.search(
            r"\{.*?\}",
            text,
            re.DOTALL,
        )

        if match:
            try:
                parsed = json.loads(match.group(0))
                return parsed if isinstance(parsed, dict) else {}
            except json.JSONDecodeError:
                pass

        return {}

    @staticmethod
    def _fallback_classify(message: str):
        text = message.lower().strip()

        if any(
            phrase in text
            for phrase in [
                "cancel my order",
                "cancel the order",
                "cancel an order",
                "cancel order",
                "want to cancel",
                "need to cancel",
            ]
        ):
            return "cancellations", 0.95

        if any(
            phrase in text
            for phrase in [
                "refund",
                "money back",
                "money hasn't come back",
                "money has not come back",
            ]
        ):
            return "refunds", 0.95

        if any(
            phrase in text
            for phrase in [
                "return this",
                "return the",
                "return a product",
                "return product",
                "return an item",
                "return item",
                "can i return",
                "can i send back",
                "send this back",
                "send it back",
                "return policy",
            ]
        ):
            return "returns", 0.95

        if any(
            phrase in text
            for phrase in [
                "payment failed",
                "payment fail",
                "card declined",
                "card was declined",
                "billing",
                "payment method",
                "credit card",
                "debit card",
                "payment problem",
                "payment issue",
            ]
        ):
            return "payments", 0.95

        if any(
            phrase in text
            for phrase in [
                "forgot my password",
                "forgot password",
                "reset my password",
                "password reset",
                "can't log in",
                "cannot log in",
                "login",
                "log in",
                "account access",
                "account compromised",
                "compromised account",
            ]
        ):
            return "account_support", 0.95

        if any(
            phrase in text
            for phrase in [
                "compatible",
                "compatibility",
                "specification",
                "specifications",
                "dimensions",
                "product details",
                "product information",
                "in stock",
                "out of stock",
                "availability",
                "accessories",
            ]
        ):
            return "product_information", 0.95

        if any(
            phrase in text
            for phrase in [
                "shipping",
                "delivery time",
                "delivery take",
                "how long does delivery",
                "how long does shipping",
                "standard shipping",
                "express shipping",
                "tracking",
                "tracking number",
                "shipping delay",
                "delivery delay",
                "when will it arrive",
                "when will my package",
            ]
        ):
            return "shipping", 0.95

        if any(
            phrase in text
            for phrase in [
                "where is my order",
                "where's my order",
                "order status",
                "track my order",
                "track order",
                "my order",
                "order number",
                "order processing",
                "order shipped",
                "order delivered",
            ]
        ):
            return "order_support", 0.95

        return "general_support", 0.50
