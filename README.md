# LLM Engineering Projects

This repository contains Python programs created as part of the [LLM Engineering: Master AI and Large Language Models](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models) course on Udemy.

## Current Projects

### 1. Website Summarizer (OpenAI)
`w1d1-site-summary.py`
- Fetches content from a given URL
- Uses OpenAI's API to generate a concise summary
- Demonstrates basic web scraping and API integration with OpenAI

### 2. Website Summarizer (Ollama)
`w1d2-site-summary-ollama.py`
- Similar functionality to the OpenAI version but uses a local Ollama instance
- Implements chat-based prompting with system and user messages
- Shows how to work with local LLMs

## Setup

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. For the OpenAI version, set your API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

3. For the Ollama version, ensure you have Ollama installed and running locally.

## Running Tests

To run the unit tests, first install the test dependencies:

```bash
pip install -r requirements-test.txt
```

Then run the tests using pytest:

```bash
# Run all tests
pytest -v

# Run tests with coverage report
pytest --cov=. --cov-report=term-missing

# Run a specific test file
pytest test_w1d1_site_summary.py -v
pytest test_w1d2_site_summary_ollama.py -v
```

The tests include:
- URL validation
- URL normalization
- Website class initialization
- Summary generation (mocked)

## Usage

Run either script to summarize the hardcoded URL:
```bash
python w1d1-site-summary.py
# or
python w1d2-site-summary-ollama.py
```

Note: The URL is currently hardcoded in the script. To change the URL, modify the `url` variable in the `main()` function.

## Course Information
These projects are part of the [LLM Engineering: Master AI and Large Language Models](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models) course on Udemy, which covers practical applications of large language models in Python.
