import subprocess
from subprocess import run

result = run(["ls", "-la"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

