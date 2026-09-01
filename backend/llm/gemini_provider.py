import json
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)


class GeminiProvider:
    """
    Gemini LLM provider for ShopAssist AI.

    Uses Google's Interactions API and extracts the response
    through the Interaction.output_text property.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash"
        )

        self.client = genai.Client(api_key=api_key)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        top_p: float = 0.9,
        tools: Optional[list] = None,
    ) -> Dict[str, Any]:

        try:
            interaction = self.client.interactions.create(
                model=self.model,
                input=user_prompt,
                system_instruction=system_prompt,
                generation_config={
                    "temperature": temperature,
                    "top_p": top_p,
                },
            )

            # The current Interactions API exposes generated text
            # through output_text.
            output_text = getattr(interaction, "output_text", None)

            if not output_text:
                raise RuntimeError(
                    "Gemini returned no output_text"
                )

            output_text = output_text.strip()

            # Try to parse structured JSON returned by the model.
            try:
                return json.loads(output_text)

            except json.JSONDecodeError:
                # Graceful fallback if the model returns plain text.
                return {
                    "intent": "general_support",
                    "answer": output_text,
                    "confidence": 0.8,
                    "sources": [],
                    "tool_used": "none",
                }

        except Exception as exc:
            print(
                f"Gemini request failed: "
                f"{type(exc).__name__}: {exc}"
            )

            raise
