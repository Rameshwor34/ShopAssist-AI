import json

from openai import OpenAI

from backend.config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    TEMPERATURE,
    TOP_P,
)
from backend.models.schemas import AssistantResponse
from backend.tools.definitions import TOOLS
from backend.tools.registry import TOOL_REGISTRY


class OpenAIProvider:

    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

        self.model = LLM_MODEL

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> AssistantResponse:

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

        first_response = self.client.chat.completions.create(
            model=self.model,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        assistant_message = first_response.choices[0].message

        if not assistant_message.tool_calls:
            return self._structured_response(messages)

        messages.append(
            assistant_message.model_dump()
        )

        for tool_call in assistant_message.tool_calls:

            function_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            tool_function = TOOL_REGISTRY.get(function_name)

            if tool_function is None:
                tool_result = {
                    "success": False,
                    "error": f"Unknown tool: {function_name}"
                }
            else:
                tool_result = tool_function(**arguments)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result),
                }
            )

        return self._structured_response(messages)

    def _structured_response(
        self,
        messages: list,
    ) -> AssistantResponse:

        completion = self.client.chat.completions.parse(
            model=self.model,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            messages=messages,
            response_format=AssistantResponse,
        )

        message = completion.choices[0].message

        if message.parsed is None:
            raise ValueError(
                "The model did not return a valid structured response."
            )

        return message.parsed