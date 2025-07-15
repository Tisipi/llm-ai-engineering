# Standard Library Imports
import json
import os
import re
from textwrap import dedent

# Third-Party Imports
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI


class Website:
    """Handles fetching and processing website content."""
    
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    def __init__(self, url):
        """
        Initialize with URL and fetch content.
        
        Args:
            url (str): The URL of the website to fetch and process
        """
        self.url = url
        self.title = None
        self.text = None
        self.links = None
        self._fetch_and_parse()
    
    def get_content(self):
        """Get the title and text content of the webpage."""
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"
    
    def _fetch_and_parse(self):
        """
        Fetch the webpage and parse its content.
        
        Sets instance variables:
            title (str): The title of the webpage
            text (str): The cleaned text content of the webpage
            links (list): List of links found on the webpage
        """
        response = requests.get(self.url, headers=self.HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        self._clean_content(soup)
        self.text = soup.body.get_text(separator="\n", strip=True)
        self.links = self._extract_links(soup)
    
    def _clean_content(self, soup):
        """
        Remove irrelevant elements from the parsed HTML.
        
        Args:
            soup: BeautifulSoup object containing the parsed HTML
        """
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
            
    def _extract_links(self, soup):
        """
        Extract all href links from the parsed HTML.
        
        Args:
            soup: BeautifulSoup object containing the parsed HTML
            
        Returns:
            list: List of href links found in the document
        """
        return [link.get('href') for link in soup.find_all('a', href=True)]


class SystemPrompts:
    """Collection of system prompts for different AI roles."""

    @staticmethod
    def brochure_links_analyzer():
        """
        Return the prompt for analyzing and categorizing relevant links for a company brochure.
        
        Returns:
            str: Prompt for identifying brochure-relevant links
        """
        return dedent("""\
            ROLE: Professional Content Analyst

            TASK:
            - Analyze the provided list of links from a company website
            - Identify which links are most relevant for a company brochure
            - Focus on pages like About, Company, Team, Careers, Services, Products, Contact
            - Ignore login, privacy policy, terms of service and other non-essential pages

            RESPONSE FORMAT:
            - Respond with a JSON object containing an array of relevant links
            - Each link should have a 'type' (e.g., 'about page', 'careers page')
            - Include the full URL in the 'url' field
            - Only include genuinely relevant links (0-5 links is typical)

            EXAMPLE RESPONSE:
            {
                "links": [
                    {"type": "about page", "url": "https://example.com/about"},
                    {"type": "careers page", "url": "https://example.com/careers"}
                ]
            }""")

    @staticmethod
    def brochure_website_analyser():
        return dedent("""\
            ROLE: Professional Content Analyst

            TASK:
            - Analyze the contents of several relevant pages from a company website
            - Create a short brochure about the company for prospective customers, investors and recruits
            - Respond in markdown
            - Include details of company culture, customers and careers/jobs if you have the information
            - Brochure must in the language of the website
            """)


class UserPrompts:
    """Collection of user prompts for different AI interactions."""
    
    @staticmethod
    def brochure_links_analyzer(website):
        """
        Generate a user prompt with website links for brochure analysis.
        
        Args:
            website: Website object containing links to analyze
            
        Returns:
            str: Formatted prompt with website links
        """
        links_text = "\n".join(website.links)
        return dedent(f"""
            Here is the list of links on the website of {website.url}.
            Please decide which of these are relevant web links for a brochure about the company.
            Respond with the full https URL in JSON format. 
            Do not include Terms of Service, Privacy, or email links.
            
            Links (some might be relative links):
            {links_text}
        """)

    @staticmethod
    def brochure_website_analyzer(website):
        """
        Generate a user prompt with website details for brochure analysis.
        
        Args:
            website: Website object with relevant links to analyze
            
        Returns:
            str: Formatted prompt with website details for brochure analysis
        """
        prompt = dedent(f"""
            You are looking at the website {website.url} of a company.
            Here are the contents of its landing page and other relevant pages; 
            use this information to build a short brochure of the company in markdown.
            {get_all_website_details(website.url)}
            Respond in markdown.
        """)
        # Truncate if more than 5,000 characters
        return prompt[:5_000]


def message_prompts_for_links_analysis(website):
    """Create the messages structure for the OpenAI API call."""
    return [
        {"role": "system", "content": SystemPrompts.brochure_links_analyzer()},
        {"role": "user", "content": UserPrompts.brochure_links_analyzer(website)}
    ]


def message_prompts_for_brochure_website_analyzer(website):
    """Create the messages structure for the OpenAI API call."""
    return [
        {"role": "system", "content": SystemPrompts.brochure_website_analyser()},
        {"role": "user", "content": UserPrompts.brochure_website_analyzer(website)}
    ]


def get_api_key():
    """Retrieve and validate the OpenAI API key."""
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    if not api_key.startswith("sk-"):
        raise ValueError("Invalid API Key. Should start with 'sk-'")
    return api_key


def ask_llm_for_relevant_links(url):
    openai = OpenAI(api_key=get_api_key())
    website = Website(url)
    print("Using openai API to fetch relevant links on the website")
    response = openai.chat.completions.create(  
        model="gpt-4o-mini",
        messages=message_prompts_for_links_analysis(website),
        response_format={"type": "json_object"}
    )
    print("Relevant links:", response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)


def get_all_website_details(url):
    result = "Landing page:\n"
    result += Website(url).get_content()
    links = ask_llm_for_relevant_links(url)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_content()
    return result


def ask_llm_to_make_brochure_from_website(url):
    """Generate a brochure from the content at the given URL."""
    print("Making brochure from website:", url)

    openai = OpenAI(api_key=get_api_key())
    website = Website(url)
    print("Using openai API to create a brochure")
    response = openai.chat.completions.create(  
        model="gpt-4o-mini",
        messages=message_prompts_for_brochure_website_analyzer(website))
    return response.choices[0].message.content


def normalize_url(url):
    """Ensure the URL has a scheme (https://)."""
    if not url.startswith(('http://', 'https://')):
        return f'https://{url}'
    return url


def is_valid_url(url):
    """
    Check if the URL is valid using a comprehensive regex pattern.

    This pattern matches:
    - Domain names (example.com)
    - Subdomains (www.example.com, blog.example.co.uk)
    - Optional http:// or https://
    - Optional paths, queries, and fragments
    """
    pattern = re.compile(
        r'^(https?:\/\/)?'  # http:// or https:// (optional)
        r'([\w-]+\.)+'     # subdomains
        r'[a-z]{2,}'          # top level domain (at least 2 chars)
        r'(:\d+)?'           # optional port number
        r'(\/[\w\-\.\/?%&=]*)?$',  # path, query parameters, etc.
        re.IGNORECASE
    )
    return bool(re.match(pattern, url))


def prompt_user_for_valid_url():
    url = None
    while True:
        url_input = input("Enter the URL to make a brochure for (e.g., www.example.com): ").strip()
        if not url_input:
            print("Error: URL cannot be empty. Please try again.\n")
            continue

        if not is_valid_url(url_input):
            print("Error: Invalid URL format. Please include a valid domain (e.g., example.com or www.example.com)\n")
            continue

        url = normalize_url(url_input)
        print(f"\nFetching and making a brochure for: {url}")
        break
    return url


def create_brochure_from_website(url):
    try:
        brochure = ask_llm_to_make_brochure_from_website(url)
        print("\nBrochure:")
        print(brochure)
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please check the URL and try again.")


def main():
    """
    Main function to run the brochure creation process.
    Prompts the user for a valid company website URL, then generates and prints a brochure using the website's content.
    """
    url = prompt_user_for_valid_url()
    create_brochure_from_website(url)


if __name__ == "__main__":
    main()