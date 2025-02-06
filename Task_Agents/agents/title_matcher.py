import os

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.gemini import GeminiModel

from Task_Agents.model import UserState
from Task_Agents.tasks import get_google_tasks



# Define a Pydantic model for the result
class Match(BaseModel):
    title: str
    id: str
    is_title_present: bool


# Create a PydanticAI instance
_model = GeminiModel('gemini-1.5-flash')
title_matcher_agent = Agent(
    _model,
    system_prompt=("You are a helpful ai assistant\n"),
    deps_type=UserState,
    result_type=Match,
    result_tool_name="title_matcher",
    result_tool_description="Identify the right title",
    result_retries=3,
)


@title_matcher_agent.system_prompt
def system_prompt(ctx: RunContext[UserState]) -> str:
    # First, we read the tasks for the user
    tasks = get_google_tasks()

    # Next, we create a dictionary of tasks
    task_dict = [{"id": task.id, "title": task.title} for task in tasks.tasks]

    # Tasnform the dict to string
    task_dict = str(task_dict)

    # Craft the system prompt
    return (
        "Identify the title provided by the user\n"
        f"The title must be present in this list: {tasks}\n\n"
        "Find the title which is the closest match to the user's input\n"
        "If no title is present, provide an empty string and mark is_title_present as False"
        "Put the id of the task in the result that you can find in this dict {task_dict}"
    )
