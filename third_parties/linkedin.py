import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    Scrape information from LinkedIn profiles.

    Args:
        linkedin_profile_url (str): The URL of the LinkedIn profile to scrape.
        mock (bool): If True, use a mock URL to avoid consuming API calls.

    Returns:
        dict: A dictionary of the scraped LinkedIn profile data.
    """

    if mock:
        # If in mock mode, use a provided Gist URL for testing
        linkedin_profile_url = "USE HERE A GIST URL TO TEST IF YOU DOT WANT TO CONSUME YOUR API CALLS"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        # API endpoint for LinkedIn scraping
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        # Retrieve the API key from environment variables and set it in headers
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        # Make an API request with the profile URL as a parameter
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )

    # Convert the response to JSON format
    data = response.json()
    # Filter out any empty or irrelevant fields
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None)
           and k not in ["people_also_viewed", "certifications"]
    }
    # Remove 'profile_pic_url' from each group entry in 'groups' field, if present
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    # Test scraping function with a LinkedIn profile URL
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/ayoub-boulidam-a1a820245/",
        )
    )

import requests
