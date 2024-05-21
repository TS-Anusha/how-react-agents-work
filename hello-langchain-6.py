from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tools.system_time_tool import *
from react_template import get_react_prompt_template
from langchain_core.output_parsers import StrOutputParser
from langchain.tools.render import render_text_description

# load environment variables
load_dotenv()

# Choose the LLM to use
llm = ChatOpenAI(model="gpt-4", model_kwargs={"stop":"\nObservation"})

# set my message
query = "What's the current time in New York?"

# set the tools
tools = [check_system_time, convert_time_zone]

# Get the react prompt template
prompt_template = get_react_prompt_template()

prompt_template = prompt_template + """I need to check the current system time. New York is generally 5 hours behind London, but this can change due to daylight saving time. Therefore, I will first find out the current time in London and then make the necessary adjustments to find the time in New York.
Action: check_system_time
Action Input: '%Y-%m-%d %H:%M:%S'""" + "\nObservation: '2024-04-07 00:58:00'" + "\nThought:"

# execute
output_parser = StrOutputParser()
chain = prompt_template | llm | output_parser

# get the tools list
tools_list=render_text_description(list(tools))
tool_names=", ".join([t.name for t in tools])

# print out the prompt
print(prompt_template.format(input=query, tools=tools_list, tool_names=tool_names, agent_scratchpad=""))

# execute
result = chain.invoke({"input": query, "tools":tools_list, "tool_names": tool_names, "agent_scratchpad": ""})
print(result)