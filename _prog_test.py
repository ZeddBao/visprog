import os
import json
from functools import partial

from engine.utils import ProgramGenerator
from prompts.gqa import create_prompt


if os.path.exists("settings.json"):
    with open("settings.json", "r") as f:
        settings = json.load(f)
        os.environ["OPENAI_API_KEY"] = settings["OPENAI_API_KEY"]
        os.environ["OPENAI_API_BASE"] = settings["OPENAI_API_BASE"]
else:
    raise Exception("settings.json not found!")

prompter = partial(create_prompt,method='all')
generator = ProgramGenerator(prompter=prompter)

question = "How many people or animals are in the image?"
# question = "Are there more animals than people in the image?"
# question = "Localize the woman and tell me the color of her dress."
# question = "Find and tell me the name of the animal in the image."
# question = "How many women are to the right of the camel?"
# question = "How many women are to the left of the camel?"
# question = "Is the lamp to the left of the woman lit?"
# question = "Is there a sun in the sky?"
prog,_ = generator.generate(dict(question=question))
print(prog)