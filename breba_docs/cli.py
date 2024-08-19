import os.path

import docker
import requests

from breba_docs.analyzer.service import analyze
from breba_docs.services.openai_agent import OpenAIAgent
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_valid_url(url):
    # TODO: check if md file
    parsed_url = urlparse(url)

    return all([parsed_url.scheme, parsed_url.netloc])


def is_file_path(path):
    return os.path.exists(path)


def run():
    load_dotenv()
    client = docker.from_env()
    started_container = client.containers.run(
        "python:3",
        command="/bin/bash",
        stdin_open=True,
        tty=True,
        detach=True,
        working_dir="/usr/src",
    )

    doc_location = input("Provide url to doc file or an absolute path:")

    errors = []
    if is_file_path(doc_location):
        with open(doc_location, "r") as file:
            document = file.read()
    elif is_valid_url(doc_location):
        response = requests.get(doc_location)
        # TODO: if response is not md file produce error message
        document = response.text
    else:
        document = None
        errors += "Not a valid url or local file path"

    if errors:
        print(errors)
    elif document:
        ai_agent = OpenAIAgent()
        analyze(ai_agent, started_container, document)
    else:
        print("Document text is empty, but no errors were found")
