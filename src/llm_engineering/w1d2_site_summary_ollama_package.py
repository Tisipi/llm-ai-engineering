# Standard Library Imports
import re
from textwrap import dedent
from urllib.parse import urlparse

# Third-Party Imports
import requests
from bs4 import BeautifulSoup
import ollama


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
        self._fetch_and_parse()
    
    def _fetch_and_parse(self):
        """
        Fetch the webpage and parse its content.
        
        Sets instance variables:
            title (str): The title of the webpage
            text (str): The cleaned text content of the webpage
        """
        response = requests.get(self.url, headers=self.HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        self._clean_content(soup)
        self.text = soup.body.get_text(separator="\n", strip=True)
    
    def _clean_content(self, soup):
        """
        Remove irrelevant elements from the parsed HTML.
        
        Args:
            soup: BeautifulSoup object containing the parsed HTML
        """
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()


class SystemPrompts:
    """Collection of system prompts for different AI roles."""
    
    @staticmethod
    def content_analyst():
        """Return the prompt for content analysis tasks."""
        PROMPT = dedent("""\
            ROLE: Professional Content Analyst

            TASK:
            - Analyze and summarize web content
            - Focus on main content, ignore navigation elements
            - Be objective, factual and professional

            FORMAT:
            - Use markdown formatting
            - Structure with clear headings
            - Use bullet points for lists
            - Bold important terms""")
        return PROMPT


def create_user_prompt(website):
    """Generate a user prompt with website content for summarization."""
    TEMPLATE = dedent("""\
        # Website Summary Request
        ## Website Title: {title}

        ## Content to Summarize:
        {content}\
    """)
    return TEMPLATE.format(title=website.title, content=website.text)


def create_messages(website):
    """Create the messages structure for the Ollama API call."""
    return [
        {"role": "system", "content": SystemPrompts.content_analyst()},
        {"role": "user", "content": create_user_prompt(website)}
    ]


def summarize_website(url):
    """Generate a summary of the content at the given URL."""
    MODEL = "llama3.2"  
    website = Website(url)
    # Use the chat function directly from the ollama package
    print("Using ollama python package")
    response = ollama.chat(model=MODEL, messages=create_messages(website))
    return response['message']['content']


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


def normalize_url(url):
    """Ensure the URL has a scheme (https://)."""
    if not url.startswith(('http://', 'https://')):
        return f'https://{url}'
    return url


def main():
    """Main function to run the website summary program."""
    while True:
        url_input = input("Enter the URL to summarize (e.g., www.example.com): ").strip()
        if not url_input:
            print("Error: URL cannot be empty. Please try again.\n")
            continue
            
        if not is_valid_url(url_input):
            print("Error: Invalid URL format. Please include a valid domain (e.g., example.com or www.example.com)\n")
            continue
            
        url = normalize_url(url_input)
        print(f"\nFetching and summarizing content of: {url}")
        break
    try:
        summary = summarize_website(url)
        print("\nSummary:")
        print(summary)
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please check the URL and try again.")


if __name__ == "__main__":
    main()