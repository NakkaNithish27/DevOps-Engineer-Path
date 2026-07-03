import subprocess

prompt = (
    "Read prompt.txt. "
    "Read Input/56-copilot-ai-for-coding.txt. "
    "Follow all instructions from prompt.txt. "
    "Do not create files. "
    "Return only the final markdown output."
)

command = (
    f'gemini --model gemini-3.1-flash-lite '
    f'--skip-trust '
    f'--prompt "{prompt}"'
)

result = subprocess.run(
    command,
    shell=True,
    capture_output=True,
    text=True,
    encoding="utf-8"
)

with open("test_output.md", "w", encoding="utf-8") as f:
    f.write(result.stdout)

print("Saved output to test_output.md")

print("\nSTDERR:")
print(result.stderr)

print("\nRETURN CODE:")
print(result.returncode)