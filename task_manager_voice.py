from time import sleep
from dotenv import load_dotenv
import logfire
import os

# Load environment variables
load_dotenv(override=True)


os.environ["CREDS_FILE"] = os.path.join(os.path.dirname(__file__), os.getenv("CREDS_FILE"))
os.environ["TOKEN_FILE"] = os.path.join(os.path.dirname(__file__), os.getenv("TOKEN_FILE"))

from Task_Agents.agents.executor import task_executor_agent
from Task_Agents.agents.intent_classifier import intent_classifier_agent
from Task_Agents.agents.task_summarizer import task_summarizer_agent
from Task_Agents.agents.title_matcher import title_matcher_agent
from Task_Agents.model import UserState
from utils.conversation_manager import conversation

# Configure logfire
logfire.configure()

# Wait for logfire to start
sleep(1)

# Create a UserState instance
user_state = UserState(id="Philippe")

#query = input("Enter your query: ")
is_finals = []
query = ""
manager = conversation()

if manager is not None:
    query = "\n".join(manager)

result = intent_classifier_agent.run_sync(query)
print(f"Identified intent: {result.data.action}")

match result.data.action:
    case "addTask":
        result = task_executor_agent.run_sync(
            "Identify the right title and add the task", deps=user_state, message_history=result.all_messages()
        )

    case "getTasks":
        result = task_executor_agent.run_sync("Get the tasks", deps=user_state, message_history=result.all_messages())
        result = task_summarizer_agent.run_sync(
            f"Summarize these tasks in a concise and oraganized manner: {result.data}", message_history=result.all_messages()
        )

    case "markTaskAsDone":
        result = title_matcher_agent.run_sync(query, deps=user_state)
        print(
            f"Title: {result.data.title}, Is title present: {result.data.is_title_present}"
        )

        if not result.data.is_title_present:
            raise Exception("Title not present")

        result = task_executor_agent.run_sync(
            f"Mark the task '{result.data.title}' as done with id '{result.data.id}'",
            deps=user_state,
        )

print(result.data)
