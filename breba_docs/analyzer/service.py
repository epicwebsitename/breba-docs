from breba_docs.services.openai_agent import OpenAIAgent
from docker.models.containers import Container


def analyze(agent: OpenAIAgent, container: Container, doc: str):

    commands = agent.fetch_commands(doc)

    chained_commands = ' && '.join(commands)

    print(f"Will run the following commands: {chained_commands}\n")

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