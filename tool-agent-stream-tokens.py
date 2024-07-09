from env import get_env
import os
import asyncio

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

async def main():
    async for event in agent_executor.astream_events({"messages": [HumanMessage(content="whats the weather in sf?")]}, version="v1"):
        kind = event["event"]

        if kind == "on_chain_start":
            if (event["name"] == "Agent"):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print(f"Starting agent: {event['name']} with input: {event['data'].get('input')}")
        elif kind == "on_chain_end":
            if (event["name"] == "Agent"):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print()
                print("--")
                print(f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}")
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content

            if content:
                # Empty content in the context of OpenAI means
                # that the model is asking for a tool to be invoked.
                # So we only print non-empty content
                print(content, end="")
        elif kind == "on_tool_start":
            print("--")
            print(f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}")
        elif kind == "on_tool_end":
            print(f"Done tool: {event['name']}")
            print(f"Tool output was: {event['data'].get('output')}")
            print("--")

asyncio.run(main())