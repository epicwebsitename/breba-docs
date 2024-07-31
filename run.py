import docker

client = docker.from_env()

# TODO: build docker image using code?
output = client.containers.run("command-runner")
print(output.decode('utf-8'))
