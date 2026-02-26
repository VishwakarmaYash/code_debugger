import json
from pathlib import Path

# Try to import `GeminiClient` from the local utils package. If optional
# dependencies are not installed (common in fresh dev environments) we
# fall back to printing the constructed prompt so the file remains useful.
try:
	from utils.llm_client import GeminiClient
except Exception:
	GeminiClient = None

prompt_path = Path("utils/prompts/debugging_prompt.json")
data = json.loads(prompt_path.read_text())

system_instruction = data["system_instruction"]
template = data["user_prompt_template"]

user_input = "print(Hello World)"

prompt = system_instruction + "\n\n" + template.replace("{{USER_INPUT}}", user_input)

if GeminiClient is None:
	print("GeminiClient unavailable — optional dependencies may be missing.")
	print("Constructed prompt:\n")
	print(prompt)
else:
	client = GeminiClient()
	print(client.ask(prompt))