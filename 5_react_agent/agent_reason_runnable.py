from langchain_openai import ChatOpenAI
from langchain.agents import tool, create_react_agent
import datetime
from langchain_community.tools import TavilySearchResults
from langchain import hub
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4")


@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Returns the current date and time in the specified format """

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

search_tool = TavilySearchResults(search_depth="basic")
react_prompt = hub.pull("hwchase17/react")

tools = [get_system_time, search_tool]

react_agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt) # which gives AgentAction or AgentFinish 
# agent_executor = AgentExecutor(agent=react_agent, tools=tools, verbose=True)
# print(agent_executor.invoke({"input": "What time is it now in New York?"}))

# agent_outcome = react_agent.invoke({"input" : "what time is it now in New York?", "intermediate_steps": []})
# print(agent_outcome)