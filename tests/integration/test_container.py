import docker
import pytest

from breba_docs.analyzer.service import execute_command


@pytest.fixture
def container():
    client = docker.from_env()

    return client.containers.run(
        "python:3",
        command="/bin/bash",
        stdin_open=True,
        tty=True,
        detach=True,
        working_dir="/usr/src",
    )


@pytest.mark.integration
def test_execute_command(container):
    command = 'echo "Some output from the command"'
    output_text = execute_command(command, container)
    assert "Some output from the command" in output_text
