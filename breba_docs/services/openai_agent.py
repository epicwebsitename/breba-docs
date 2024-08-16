from openai import OpenAI


class OpenAIAgent:
    INSTRUCTIONS = """
    You are assisting a software program to validate contents of a document.  Here are important instructions:
    0) Never return markdown. You will either return text without special formatting
    1) The user is usually expecting a list of commands that will be run in  the terminal sequentially. Return a comma separated list only.
    2) The user may present you with output in that case you will answer with either, "ERROR" if the response contains an 
    error, "PASS" if the response is valid, or "UNKNOWN" if it is not clear whether the output is correct.
    3) When reading the document, you will only use terminal commands in the document exactly as they are written 
    in the document even if there are typos or errors.
    """

    def __init__(self):
        self.client = OpenAI()

        self.assistant = self.client.beta.assistants.create(
            name="Breba Docs",
            instructions=OpenAIAgent.INSTRUCTIONS,
            model="gpt-4o-mini"
        )

        self.thread = self.client.beta.threads.create()

    def do_run(self, message, instructions):
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions=instructions
        )

        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            # TODO: validate that commands are actually commands
            return messages.data[0].content[0].text.value
        else:
            print(run.status)


    def fetch_commands(self, text):
        # TODO: Verify that this is even a document file.
        message = "Here is the documentation file. Please provide a comma separated list of commands that can be run in the terminal:\n"
        message += text
        return self.do_run(text, "").split(",")


    def analyze_output(self, text):
        return ("Found some errors. Looks like cd my_project is failing to execute with the following error: cd "
                "command not found")