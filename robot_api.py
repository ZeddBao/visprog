import os
import sys
import json
from typing import List, Dict
from functools import partial

import cv2
import numpy as np
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
    with open('settings.json', 'w'):
        print("Please fill in your OpenAI API key and base URL in settings.json.")
        exit()


def parse_obj(query_obj: str, image: Image, inspect=False) -> List[Dict[np.array, str, List[int], int]]:
    """
    :param: query_obj: the name of the object
    :param: image: the image to be queried
    :return: [{'mask': array([[0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.],
       ...,
       [0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.]], dtype=float32), 'category': category, 'box': [x1, y1, x2, y2], 'inst_id': inst_id}] object list
    """

    # Get the initial size of the picture
    width, height = image.size

    interpreter = ProgramInterpreter(dataset='objQuery')
    prompter = partial(create_prompt, method='all')
    generator = ProgramGenerator(prompter=prompter)

    image.thumbnail((640, 640), Image.Resampling.LANCZOS)
    init_state = dict(
        IMAGE=image.convert('RGB')
    )

    prog, _ = generator.generate(dict(question=query_obj))
    if inspect:
        print(prog)

    result, prog_state = interpreter.execute(prog, init_state, inspect=False)
    if inspect:
        print(prog_state)

    # Scale the bounding box to the original size
    for obj in result:
        obj['box'] = [i * width // 640 for i in obj['box']]
        obj['mask'] = cv2.resize(
            obj['mask'], image.size, interpolation=cv2.INTER_NEAREST)

    return result


if __name__ == "__main__":
    image = Image.open('assets/duck.png')
    result = parse_obj('duck', image, inspect=False)
    print(result)
