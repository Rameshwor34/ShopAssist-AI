from typing import List, Optional

from pydantic import BaseModel, Field


class AssistantResponse(BaseModel):

    intent: str = Field(
        description="The user's detected intent."
    )

    answer: str = Field(
        description="The assistant's answer."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence from 0 to 1."
    )

    sources: List[str] = Field(
        default_factory=list,
        description="Sources used to answer the question."
    )

    tool_used: Optional[str] = Field(
        default=None,
        description="Name of the tool used, if any."
    )