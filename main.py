from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain_openai import AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentType, AgentExecutor


load_dotenv()
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm= ChatOpenAI (model="gpt-4o-mini")
#llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
#response = llm.invoke("what life style changes are essential for long living?")
#print(response)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a research assistant. Given a research topic, you will provide a concise summary, list of sources, and tools used in the research. Format the output as per the ResearchResponse schema.\n{format_instructions}"
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=[]
)
agent_exc = AgentExecutor(agent=agent,tools=[],verbose=True)
raw_response = agent_exc.invoke({"query": "Explain to a 5 year old the histroy of color making. "})
print(raw_response)
response = parser.parse(raw_response.get("output"))
print(response)