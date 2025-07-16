# LLM Engineering Projects

This repository contains Python programs created as part of the [LLM Engineering: Master AI and Large Language Models](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models) course on Udemy. The course covers practical applications of large language models in Python.

## Current Projects

### 1. Website Summarizer (OpenAI)
`w1d1_site_summary.py`
- Fetches content from a given URL
- Uses OpenAI's API to generate a concise summary
- Demonstrates basic web scraping and API integration with OpenAI

```bash
python src/llm_engineering/w1d1_site_summary.py
```

### 2. Website Summarizer (Ollama)
`w1d2_site_summary_ollama.py`
- Similar functionality to the OpenAI version but uses a local Ollama instance
- Implements chat-based prompting with system and user messages
- Shows how to work with local LLMs

```bash
python src/llm_engineering/w1d2_site_summary_ollama.py
```

### 3. Website Summarizer (Ollama Package)
`w1d2_site_summary_ollama_package.py`
- Similar functionality to the OpenAI version but uses a local Ollama instance
- Uses the official Ollama Python package for API integration
- Implements chat-based prompting with system and user messages
- Shows how to work with local LLMs

```bash
python src/llm_engineering/w1d2_site_summary_ollama_package.py
```

### 4. Website Summarizer (Ollama via OpenAI Client)
`w1d2_site_summary_ollama_openai.py`
- Similar functionality to the OpenAI version but uses a local Ollama instance
- Uses the OpenAI client library to connect to a local Ollama instance
- Demonstrates how to use the OpenAI client with alternative LLM backends
- Implements chat-based prompting with system and user messages
- Shows how to work with local LLMs

```bash
python src/llm_engineering/w1d2_site_summary_ollama_openai.py
```

### 5. Website Brochure Generator
`w1d5_site_brochure.py`
- Analyzes a company website and generates a professional brochure
- Uses OpenAI's API to fetch relevant links on the website
- Uses OpenAI's API to generate a brochure from the content of the relevant links of the website
- Demonstrates structured JSON responses from the LLM

```bash
python src/llm_engineering/w1d5_site_brochure.py
```

### 6. Website Brochure Generator (Streaming)
`w1d5_site_brochure_streaming.py`
- Similar functionality as the brochure generator above but uses streaming
- Analyzes a company website and generates a professional brochure
- Uses OpenAI's API to fetch relevant links on the website
- Uses OpenAI's API to generate a brochure from the content of the relevant links of the website

```bash
python src/llm_engineering/w1d5_site_brochure_streaming.py
```

## Setup

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. For the OpenAI version, set your API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

3. For the Ollama versions, ensure you have Ollama installed and running locally.


## Usage

Each script is designed to be run independently. Follow the instructions in each script's section above for specific usage details.

