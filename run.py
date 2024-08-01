import docker

client = docker.from_env()

container = client.containers.run(
    "python:3",
    command="/bin/bash",
    stdin_open=True,
    tty=True,
    detach=True,
    working_dir="/usr/src",
)

commands = [
    "pipa install nodestream",
    "nodestream new --database neo4j my_project",
    "cd my_project",
    "nodestream run sample -v",
]

chained_commands = ' && '.join(commands)

# Execute a command in the container with real-time output
exit_code, output = container.exec_run(
    f'/bin/bash -c "{chained_commands}"',
    stdout=True,
    stderr=True,
    tty=True,
    stream=True,
)

# Print the output line by line
for line in output:
    print(line.decode('utf-8').strip())

result = container.exec_run('ls -la')
print(result.output.decode('utf-8'))

container.stop()
container.remove()
