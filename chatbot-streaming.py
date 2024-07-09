from env import get_env
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

os.environ["OPENAI_API_KEY"] = get_env("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-3.5-turbo")

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

result = prompt.invoke({"messages": [], "language": "Português"})
print("Resultado do prompt: ", result)

chain = prompt | model

with_message_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="messages")

config = {"configurable": {"session_id": "abc5"}}

message = HumanMessage(content="hi! I'm todd. tell me how to make an omelette")
for r in with_message_history.stream({ "messages": [message], "language": "Português" }, config=config):
    print(r.content, end="")

