import os

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.gemini import GeminiModel


# Create a PydanticAI instance
_model = GeminiModel('gemini-1.5-flash')

task_summarizer_agent = Agent(
    _model,
    system_prompt="You are a helpful AI assitant and a productivity expert. You always respond with motivational and helpful messages.",
)
