# Automated GitHub Analysis

A Flask-based web application that leverages OpenAI and LangChain to analyze a GitHub user's repositories and identify the most technically complex project.

Table of Contents
-----------------
- Features
- Prerequisites
- Installation
- Configuration
- Usage
- Project Structure
- Technology Stack
- Troubleshooting
- Contributing
- License

Features
--------
- Fetch up to 5 public repositories from a GitHub user
- Extract and convert code files including Jupyter notebooks
- Generate embeddings using OpenAI for code snippets
- Perform conversational code complexity analysis with LangChain and ChromaDB
- Display results in a simple Flask web interface

Prerequisites
-------------
- Python 3.7 or higher
- GitHub Personal Access Token with repo scope
- OpenAI API Key

Installation
------------
1. Clone the repository:
   git clone https://github.com/yourusername/automated-github-analysis.git
   cd automated-github-analysis
2. (Optional) Create and activate a virtual environment:
   python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt

Configuration
-------------
Set the required environment variables:
export GITHUB_TOKEN=your_github_personal_access_token
export OPENAI_API_KEY=your_openai_api_key

Usage
-----
1. Start the Flask application:
   python app.py
2. Open your browser and go to http://127.0.0.1:5000
3. Enter a GitHub profile URL such as https://www.github.com/username and click Start
4. The app will analyze the first 5 public repositories and display the most technically complex one with a description

Project Structure
-----------------
- app.py: Flask application entrypoint
- requirements.txt: Dependency list
- src/utils.py: Utility functions (URL validation, notebook conversion, text processing)
- src/userinfo.py: GitHub API integration for fetching repository data
- templates/index.html: Web UI template
- temp/: Temporary files for notebook conversion

Technology Stack
----------------
- Python
- Flask
- Requests
- LangChain
- ChromaDB
- OpenAI API
- nbconvert

Troubleshooting
---------------
- Invalid GitHub URL: use https://www.github.com/username format
- No public repositories: user may have none or repositories may be private
- API rate limits: verify GitHub token and usage
- OpenAI errors: check API key and quota



