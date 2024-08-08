import docker

from breba_docs.services.openai_agent import OpenAIAgent
from services.mock_agent import MockAgent
from dotenv import load_dotenv
from openai import OpenAI


def run(agent, container, doc):

    commands = agent.fetch_commands(doc)

    chained_commands = ' && '.join(commands)

    # Execute a command in the container with real-time output
    exit_code, output = container.exec_run(
        f'/bin/bash -c "{chained_commands}"',
        stdout=True,
        stderr=True,
        tty=True,
        stream=True,
    )

    output_text = ""

    for line in output:
        line_text = line.decode("utf-8")
        print(line_text.strip())
        output_text += line_text

    print(agent.analyze_output(output_text))

    result = container.exec_run('ls -la')
    print(result.output.decode('utf-8'))

    container.stop()
    container.remove()


if __name__ == "__main__":
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

    doc_file = "breba_docs/sample_doc.txt"

    with open(doc_file, "r") as file:
        document = file.read()

    ai_agent = OpenAIAgent()
    run(ai_agent, started_container, document)

