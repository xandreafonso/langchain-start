import os
from env import get_env

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage, SystemMessage

from langchain_core.output_parsers import StrOutputParser

os.environ["OPENAI_API_KEY"] = get_env("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = get_env("GROQ_API_KEY")

model = ChatOpenAI(model="gpt-3.5-turbo") # model = ChatGroq(model="llama3-8b-8192")

messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]

response = model.invoke(messages)

parser = StrOutputParser()
content = parser.invoke(response)

print("Primeira saída:")
print(content)

chain = model | parser

content = chain.invoke(messages)

print("Segunda saída:")
print(content)