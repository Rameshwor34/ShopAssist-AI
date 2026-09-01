import os

from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "gemini"
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "gpt-4o-mini"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

TEMPERATURE = float(
    os.getenv("TEMPERATURE", "0.2")
)

TOP_P = float(
    os.getenv("TOP_P", "0.9")
)