from langchain_community.tools.tavily_search import \
    TavilySearchResults  # Importing Tavily search tool for retrieving search results


# Function to retrieve a LinkedIn or Twitter profile URL based on a person's name
def get_profile_url_tavily(name: str):
    """
    Searches for the LinkedIn or Twitter profile page of an individual.

    Args:
        name (str): The name of the individual to search for.

    Returns:
        The search results from Tavily, which may include links to social media profiles.
    """

    # Initialize the TavilySearchResults object, which provides search functionality
    search = TavilySearchResults()

    # Run the search using the provided name as the query, which searches for the person's profile
    res = search.run(f"{name}")

    # Return the search results, which may contain URLs to LinkedIn or Twitter profiles
    return res
