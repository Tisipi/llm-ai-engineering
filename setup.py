from setuptools import setup, find_packages

setup(
    name="llm_engineering",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "python-dotenv>=1.0.0",
        "openai>=1.0.0",
    ],
    python_requires=">=3.8",
)
