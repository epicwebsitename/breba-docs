class MockAgent:
    def fetch_commands(self, text):
        return [
            "pip install nodestream",
            "nodestream new --database neo4j my_project",
            "cd my_project",
            "nodestream run sample -v",
        ]

    def analyze_output(self, text):
        return ("Found some errors. Looks like cd my_project is failing to execute with the following error: cd "
                "command not found")
