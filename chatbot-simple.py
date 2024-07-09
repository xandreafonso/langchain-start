from env import get_env
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


os.environ["OPENAI_API_KEY"] = get_env("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-3.5-turbo")

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]

with_message_history = RunnableWithMessageHistory(model, get_session_history)

config = {"configurable": {"session_id": "abc2"}}

message = HumanMessage(content="Hi! I'm Bob")
response = with_message_history.invoke([message], config=config)
print("Human:", message.content, "AI: ", response.content)

message = HumanMessage(content="What's my name?")
response = with_message_history.invoke([message], config=config)
print("Human:", message.content, "AI: ", response.content)



