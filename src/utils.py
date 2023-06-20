import re
import openai
import os
import yaml
import nbformat
from nbconvert import PythonExporter

def validate_github_url(url):
    pattern = r"https:\/\/www\.github\.com\/[A-Za-z0-9_-]+$"
    match = re.match(pattern, url)
    return bool(match)

def get_gpt_response(prompt):
    response=openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    max_tokens=500  # Adjust the max_tokens parameter to control the response length,
    )
    return response.choices[0].text.strip()

def convert_ipynb_to_py(ipynb_file, py_file):
    with open(ipynb_file, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)

    exporter = PythonExporter()
    source_code, _ = exporter.from_notebook_node(nb)
    with open(py_file, 'w', encoding='utf-8') as f:
        f.write(source_code)

import re
def reduce_token_size(code):
    # Remove leading and trailing whitespace
    code = code.strip()

    # Remove excessive line breaks
    code = re.sub(r'\n+', '\n\n', code)

    # # Remove comments
    # code = re.sub(r'#.*', '', code)  # Remove inline comments
    # code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)  # Remove multi-line comments enclosed in triple quotes
    # code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)  # Remove multi-line comments enclosed in triple single quotes
    # code = re.sub(r'//.*', '', code)  # Remove single-line comments starting with //
    # code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # Remove multi-line comments enclosed in /* */
    # Remove unnecessary whitespace
    code = re.sub(r'\s+', ' ', code)
    return code



def extract_result_and_description(text):
    result_match = re.search(r"Result:\s*(.*?)\s*Description:", text)
    description_match = re.search(r"Description:\s*(.*)$", text)

    result = result_match.group(1) if result_match else None
    description = description_match.group(1) if description_match else None

    return result, description