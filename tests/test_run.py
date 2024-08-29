from breba_docs.analyzer.service import analyze
from breba_docs.services.mock_agent import MockAgent


def test_cli(mocker):
    mock_container = mocker.MagicMock()

    def mock_exec_run(command, stdout=True, stderr=True, tty=True, stream=False):
        if stream:
            return 0, iter([b'command1\n', b'command2\n'])
        else:
            mock_result = mocker.MagicMock()
            mock_result.exit_code = 0
            mock_result.output = b'command1\ncommand2\n'
            return mock_result

    mock_container.exec_run.side_effect = mock_exec_run

    # Mock agent's fetch_commands and analyze_output methods
    agent = MockAgent()
    agent.fetch_commands = mocker.MagicMock(return_value=["echo 'command1'", "echo 'command2'"])
    agent.analyze_output = mocker.MagicMock(return_value="Analysis result")

    # Call the run function with the mock agent and mock container
    analyze(agent, mock_container, "first run echo 'command1', then run echo 'command2'")

    # Check that exec_run was called with the expected chained commands
    chained_commands = "echo 'command1' && echo 'command2'"
    mock_container.exec_run.assert_any_call(
        """/bin/bash -c 'echo '"'"'echo '"'"'command1'"'"''"'"' && echo '"'"'command1'"'"' && echo '"'"'echo \
'"'"'command2'"'"''"'"' && echo '"'"'command2'"'"''""",
        stdout=True,
        stderr=True,
        tty=True,
        stream=True
    )
