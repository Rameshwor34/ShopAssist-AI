from typing import Dict, Any, Optional
import re

from backend.agents.agents import get_agent_instruction
from backend.llm.gemini_provider import GeminiProvider
from backend.llm.prompts import SYSTEM_PROMPT
from backend.rag.retrieval import retrieve, format_context
from backend.routing.router import IntentRouter
from backend.tools.registry import TOOL_REGISTRY


class ChatService:
    """
    Production orchestration layer for ShopAssist AI.

    Pipeline:

        User request
             |
             v
        Intent Router
             |
             v
        Specialized Agent
             |
        +----+----+
        |         |
      Tool       RAG
        |         |
        +----+----+
             |
             v
        Gemini / deterministic fallback
             |
             v
        Structured response
    """

    def __init__(self):
        self.router = IntentRouter()
        self.provider = GeminiProvider()

    @staticmethod
    def _extract_order_id(message: str) -> Optional[str]:
        match = re.search(
            r"\bORD-\d+\b",
            message,
            re.IGNORECASE,
        )
        return match.group(0).upper() if match else None

    @staticmethod
    def _extract_product_id(message: str) -> Optional[str]:
        match = re.search(
            r"\bPROD-\d+\b",
            message,
            re.IGNORECASE,
        )
        return match.group(0).upper() if match else None

    def _execute_tool(
        self,
        message: str,
        intent: str,
    ) -> tuple[str, Optional[dict]]:

        order_id = self._extract_order_id(message)
        product_id = self._extract_product_id(message)

        if intent == "order_support" and order_id:
            return (
                "get_order_status",
                TOOL_REGISTRY["get_order_status"](order_id),
            )

        if intent == "product_information" and product_id:
            return (
                "get_product_info",
                TOOL_REGISTRY["get_product_info"](product_id),
            )

        if intent == "returns" and order_id:
            return (
                "check_return_eligibility",
                TOOL_REGISTRY["check_return_eligibility"](order_id),
            )

        return "none", None

    @staticmethod
    def _deterministic_answer(
        intent: str,
        tool_used: str,
        tool_result: Optional[dict],
    ) -> str:

        # -------------------------------------------------
        # Tool-based answers
        # -------------------------------------------------

        if tool_result:

            if not tool_result.get("success"):
                return tool_result.get(
                    "error",
                    "The requested information could not be found.",
                )

            if tool_used == "get_order_status":
                order = tool_result["order"]

                answer = (
                    f"Your order {order['order_id']} is currently "
                    f"{order['status']}. "
                )

                if order.get("carrier"):
                    answer += (
                        f"The carrier is {order['carrier']}. "
                    )

                if order.get("tracking_number"):
                    answer += (
                        f"Your tracking number is "
                        f"{order['tracking_number']}. "
                    )

                if order.get("estimated_delivery"):
                    answer += (
                        f"The estimated delivery date is "
                        f"{order['estimated_delivery']}."
                    )

                return answer.strip()

            if tool_used == "get_product_info":
                product = tool_result["product"]

                stock = product.get("stock", 0)

                availability = (
                    f"{stock} units are currently in stock."
                    if stock > 0
                    else "The product is currently out of stock."
                )

                return (
                    f"{product['name']} costs "
                    f"${product['price']:.2f}. "
                    f"{availability} "
                    f"{product.get('description', '')}"
                ).strip()

            if tool_used == "check_return_eligibility":
                if tool_result.get("eligible"):
                    return (
                        "Yes. This order is currently eligible "
                        "for return under the available return policy."
                    )

                return (
                    "This order is not currently eligible for return. "
                    f"{tool_result.get('reason', '')}"
                ).strip()

        # -------------------------------------------------
        # Useful deterministic fallback answers
        # -------------------------------------------------

        fallback_answers = {
            "order_support": (
                "I can help you check your order status. "
                "Please provide your order ID, for example ORD-1001."
            ),

            "shipping": (
                "I can help with shipping and delivery information. "
                "Please tell me what you would like to know, such as "
                "delivery time, shipping options, or tracking."
            ),

            "returns": (
                "I can help you with a return. "
                "Please provide your order ID so I can check whether "
                "the order is eligible for return."
            ),

            "refunds": (
                "I can help you with a refund. "
                "Please provide your order ID or tell me whether you "
                "are asking about refund eligibility or an existing refund."
            ),

            "cancellations": (
                "I can help you with an order cancellation. "
                "Please provide your order ID so I can check the order "
                "and determine the next steps."
            ),

            "payments": (
                "I can help with payment issues. "
                "Please describe the payment problem, such as a declined "
                "card, failed payment, or billing issue. "
                "Never share your full card number or CVV."
            ),

            "account_support": (
                "I can help with account access and login problems. "
                "Please describe the issue you are experiencing. "
                "Never share your password or verification codes."
            ),

            "product_information": (
                "I can help you find product information such as "
                "availability, specifications, compatibility, dimensions, "
                "and included accessories. Please provide the product ID "
                "if you have one."
            ),

            "general_support": (
                "I can help with orders, shipping, returns, refunds, "
                "payments, accounts, and product information. "
                "What would you like help with?"
            ),
        }

        return fallback_answers.get(
            intent,
            fallback_answers["general_support"],
        )

    def process(self, message: str) -> Dict[str, Any]:

        if not message or not message.strip():
            raise ValueError("Message cannot be empty.")

        message = message.strip()

        # -----------------------------------------------------
        # 1. Intent routing
        # -----------------------------------------------------

        routing = self.router.route(message)

        intent = routing["intent"]
        routing_confidence = routing["confidence"]
        routing_method = routing.get(
            "routing_method",
            "unknown",
        )

        # -----------------------------------------------------
        # 2. Execute relevant tool
        # -----------------------------------------------------

        tool_used, tool_result = self._execute_tool(
            message=message,
            intent=intent,
        )

        # -----------------------------------------------------
        # 3. Retrieve relevant knowledge
        # -----------------------------------------------------

        results = retrieve(
            message,
            top_k=3,
        )

        context = format_context(results)

        sources = []

        for result in results:
            metadata = result.get("metadata") or {}
            filename = metadata.get("filename")

            if filename and filename not in sources:
                sources.append(filename)

        # -----------------------------------------------------
        # 4. Specialized agent
        # -----------------------------------------------------

        agent_instruction = get_agent_instruction(intent)

        # -----------------------------------------------------
        # 5. Tool context
        # -----------------------------------------------------

        if tool_result is not None:
            tool_context = (
                "TOOL EXECUTION RESULT:\n"
                f"Tool: {tool_used}\n"
                f"Result: {tool_result}"
            )
        else:
            tool_context = (
                "TOOL EXECUTION RESULT:\n"
                "No tool was required or sufficient "
                "identifiers were not provided."
            )

        # -----------------------------------------------------
        # 6. Grounded prompt
        # -----------------------------------------------------

        user_prompt = f"""
CUSTOMER MESSAGE:
{message}

DETECTED INTENT:
{intent}

SPECIALIZED AGENT INSTRUCTIONS:
{agent_instruction}

RETRIEVED KNOWLEDGE BASE CONTEXT:
{context}

{tool_context}

Answer the customer's question using the available
knowledge and tool result.

Important:
- Do not invent policies.
- Do not invent customer/order/product information.
- Treat tool results as authoritative for mock transactional data.
- Use retrieved knowledge for policy and FAQ information.
- If the knowledge base and tools are insufficient, say so clearly.
- Protect sensitive information.
- Never request passwords, CVV codes, or complete card numbers.
- Keep the answer concise and useful.

Return valid JSON with exactly these fields:

{{
  "intent": "{intent}",
  "answer": "customer-facing answer",
  "confidence": 0.0,
  "sources": {sources},
  "tool_used": "{tool_used}"
}}
"""

        # -----------------------------------------------------
        # 7. Gemini generation with graceful fallback
        # -----------------------------------------------------

        try:
            response = self.provider.generate(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt,
                temperature=0.2,
                top_p=0.9,
            )

            if not isinstance(response, dict):
                response = {}

            generation_method = "gemini"

        except Exception as exc:
            print(
                f"Gemini generation unavailable; "
                f"using deterministic fallback: "
                f"{type(exc).__name__}: {exc}"
            )

            response = {
                "answer": self._deterministic_answer(
                    intent=intent,
                    tool_used=tool_used,
                    tool_result=tool_result,
                ),
                "confidence": routing_confidence,
                "sources": sources,
                "tool_used": tool_used,
            }

            generation_method = "deterministic_fallback"

        # -----------------------------------------------------
        # 8. Normalize structured response
        # -----------------------------------------------------

        response["intent"] = intent

        try:
            response["confidence"] = float(
                response.get(
                    "confidence",
                    routing_confidence,
                )
            )
        except (TypeError, ValueError):
            response["confidence"] = routing_confidence

        response["confidence"] = max(
            0.0,
            min(
                1.0,
                response["confidence"],
            ),
        )

        if not response.get("sources"):
            response["sources"] = sources

        response["tool_used"] = tool_used

        response["routing_method"] = routing_method

        response["generation_method"] = generation_method

        response.setdefault(
            "answer",
            self._deterministic_answer(
                intent=intent,
                tool_used=tool_used,
                tool_result=tool_result,
            ),
        )

        return response
