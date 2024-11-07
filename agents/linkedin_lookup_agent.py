from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.tools import get_profile_url_tavily
import re

# Load environment variables from .env file
load_dotenv()


def lookup(name: str) -> str:
    # Initialize language model
    llm = ChatGroq(
        model="mixtral-8x7b-32768",
        temperature=0,
    )

    # Define prompt template to request only a URL from the language model
    template = """Given the full name {name_of_person}, provide only the direct URL to their LinkedIn profile page (no posts or articles). Respond with the URL only, without any additional text or commentary."""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    # Define tools available for the agent, including the LinkedIn profile lookup function
    tools_for_agent = [
        Tool(
            name="Crawl Google for LinkedIn profile page",
            func=get_profile_url_tavily,
            description="Useful for when you need to get the LinkedIn Page URL",
        )
    ]

    # Load a pre-defined prompt for the REACT agent
    react_prompt = hub.pull("hwchase17/react")

    # Create a REACT agent with error handling for output parsing
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True)

    # Use the prompt template to format the input
    formatted_prompt = prompt_template.format_prompt(name_of_person=name)

    # Invoke the agent to get a result
    result = agent_executor.invoke(input={"input": formatted_prompt})

    # Extract URL from the output using regular expression to handle unexpected formatting
    result_text = result["output"]
    url_match = re.search(r'(https?://[^\s]+)', result_text)
    linked_profile_url = url_match.group(0) if url_match else "URL not found"

    return linked_profile_url


if __name__ == "__main__":
    # Test the lookup function
    print(lookup(name="Ayoub Boulidam"))
