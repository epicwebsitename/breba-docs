import docker

from services.mock_agent import MockAgent


def run(agent, container):

    commands = agent.fetch_commands("some document text")

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
    client = docker.from_env()
    started_container = client.containers.run(
        "python:3",
        command="/bin/bash",
        stdin_open=True,
        tty=True,
        detach=True,
        working_dir="/usr/src",
    )

    run(MockAgent(), started_container)

