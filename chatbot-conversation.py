import os
from env import get_env

from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

os.environ["OPENAI_API_KEY"] = get_env("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-3.5-turbo")

chat_history = []
chat_history.append(SystemMessage(content="You are a helpful AI assistant.")) 

while True:
    query = input("You: ")

    if query.lower() == "exit":
        break

    chat_history.append(HumanMessage(content=query))

    result = model.invoke(chat_history)
    response = result.content

    chat_history.append(AIMessage(content=response))

    print(f"AI: {response}")


print("---- Message History ----")
print(chat_history)