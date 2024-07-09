from env import get_env
import os

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent

os.environ["OPENAI_API_KEY"] = get_env("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"] = get_env("TAVILY_API_KEY")

model = ChatOpenAI(model="gpt-3.5-turbo")
search = TavilySearchResults(max_results=2)
tools = [search]

agent_executor = create_react_agent(model, tools)

for chunk in agent_executor.stream({"messages": [HumanMessage(content="whats the weather in sf?")]}):
    print(chunk)
    print("----")
