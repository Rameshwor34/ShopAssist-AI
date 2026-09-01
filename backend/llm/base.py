from abc import ABC, abstractmethod

from backend.models.schemas import AssistantResponse


class LLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> AssistantResponse:
        pass