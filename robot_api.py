import os
import sys
import json
from typing import List
from functools import partial

from PIL import Image

from engine.utils import ProgramGenerator, ProgramInterpreter
from prompts.objquery import create_prompt


module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

if os.path.exists("settings.json"):
    with open("settings.json", "r") as f:
        settings = json.load(f)
        os.environ["OPENAI_API_KEY"] = settings["OPENAI_API_KEY"]
        os.environ["OPENAI_API_BASE"] = settings["OPENAI_API_BASE"]
else:
    raise Exception("settings.json not found!")

def parse_obj(query_obj:str, image:Image, inspect=False) -> List[List[int]]:
    """
    :param: query_obj: the name of the object
    :param: image: the image to be queried
    :return: [[x1,y1,x2,y2],...] bounding box list
    """

    # Get the initial size of the picture
    width, height = image.size

    interpreter = ProgramInterpreter(dataset='objQuery')
    prompter = partial(create_prompt,method='all')
    generator = ProgramGenerator(prompter=prompter)

    image.thumbnail((640,640),Image.Resampling.LANCZOS)
    init_state = dict(
        IMAGE=image.convert('RGB')
    )

    prog,_ = generator.generate(dict(question=query_obj))
    if inspect:
        print(prog)

    result, prog_state = interpreter.execute(prog,init_state,inspect=False)
    if inspect:
        print(prog_state)

    # Scale the bounding box to the original size
    for bbox in result:
        bbox = [i * width // 640 for i in bbox]

    return result


if __name__ == "__main__":
    image = Image.open('assets/duck.png')
    result = parse_obj('duck',image,inspect=True)
    print(result)