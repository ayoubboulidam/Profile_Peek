from typing import Tuple, List  # Import type hints for function return types

from dotenv import load_dotenv  # Load environment variables from .env file
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

# Import LinkedIn scraping and lookup functions
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

# Import the summary parser and summary data structure
from output_parsers import summary_parser, Summary  # Ensure this parser is available


def ProfilePeek(name: str) -> Tuple[Summary, str, List[str], List[str]]:
    """
    Searches for a LinkedIn profile URL based on a name, scrapes LinkedIn data,
    and generates a profile summary, interesting facts, icebreakers, and topics.

    Args:
        name (str): The name of the person to search for on LinkedIn.

    Returns:
        Tuple: Contains the profile summary, profile picture URL, list of icebreakers,
               and list of topics of interest.
    """
    # Use LinkedIn lookup agent to retrieve the profile URL based on name
    linkedin_username = linkedin_lookup_agent(name=name)

    # Retrieve LinkedIn data (use mock=True for testing)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username,
        mock=True
    )

    # Define the template for creating a summary from LinkedIn data
    summary_template = """
       Given the LinkedIn information {information} about {name}, create:
       1. A short summary
       2. Two interesting facts about them
       3. Three icebreakers
       4. Three topics of interest

       \n{format_instructions}
    """

    # Initialize the prompt template with placeholders
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "name"],
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    # Initialize the language model
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        temperature=0,
    )

    # Create a processing chain using the | operator
    chain = summary_prompt_template | llm | summary_parser

    # Run the chain with LinkedIn data as input
    res = chain.invoke(input={"information": linkedin_data, "name": name})

    # Extract the profile picture URL from LinkedIn data
    profile_pic_url = linkedin_data.get("profile_pic_url")

    # Extract fields from the generated summary object
    ice_breakers = res.ice_breakers
    topics_of_interest = res.topics_of_interest

    return res, profile_pic_url, ice_breakers, topics_of_interest


# Main execution block to test the code
if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Test the ProfilePeek function with a sample name
    result = ProfilePeek(name="Ayoub Boulidam")
    print("Profile Summary:", result[0])
    print("Profile Picture URL:", result[1])
    print("Ice Breakers:", result[2])
    print("Topics of Interest:", result[3])
