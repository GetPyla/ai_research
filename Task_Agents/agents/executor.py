import os

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.gemini import GeminiModel

from Task_Agents.model import UserState
from Task_Agents.tasks import create_google_task as tool_add_task
from Task_Agents.tasks import complete_google_task as tool_mark_task_as_done
from Task_Agents.tasks import get_google_tasks as tool_read_tasks
from Task_Agents.tasks import Task




_model = GeminiModel('gemini-1.5-flash')
task_executor_agent = Agent(
    _model,
    system_prompt=(
        "You are a helpful ai assistant\n"
        "Follow the entire conversation history carefully to identify the tool to call and arguments to pass to them."
        "Do not call the function if the action is already performed"
    ),
    deps_type=UserState,
)


@task_executor_agent.tool
def read_tasks(ctx: RunContext[UserState]) -> str:
    """
    Reads all tasks
    """
    return f"Here's all the requested tasks:\n{tool_read_tasks(ctx.deps.id)}"


@task_executor_agent.tool
def add_task(ctx: RunContext[UserState], title: str) -> Task | None:
    """
    Appends a new task to the task list

    Args:
        title (str): The title of the new task to add.
    """

    task = Task(title=title) 

    return tool_add_task(task)


@task_executor_agent.tool
def mark_task_as_done(ctx: RunContext[UserState], id: str) -> Task | None:
    """
    Marks a task as done in the task list

    Args:
        title (str): The title of the task to mark as done.
    """
    return tool_mark_task_as_done(id)
