import random

OBJQUERY_CURATED_EXAMPLES=[
"""Question:the second yellow duck from left
BOX0=LOC(image=IMAGE,object='yellow duck')
BOX1=SORT(box=BOX0,key='lambda x: x[0]',reverse=False)
BOX2=INDEX(box=BOX1,index=1)
FINAL_RESULT=RESULT(var=BOX2)
"""
,
"""Question:the third cup from bottom
BOX0=LOC(image=IMAGE,object='cup')
BOX1=SORT(box=BOX0,key='lambda x: x[3]',reverse=True)
BOX2=INDEX(box=BOX1,index=2)
FINAL_RESULT=RESULT(var=BOX2)
"""
,
"""Question:the first duck from right
BOX0=LOC(image=IMAGE,object='duck')
BOX1=SORT(box=BOX0,key='lambda x: x[2]',reverse=True)
BOX2=INDEX(box=BOX1,index=0)
FINAL_RESULT=RESULT(var=BOX2)
"""
,
"""Question:the second duck from top
BOX0=LOC(image=IMAGE,object='duck')
BOX1=SORT(box=BOX0,key='lambda x: x[1]',reverse=False)
BOX2=INDEX(box=BOX1,index=1)
FINAL_RESULT=RESULT(var=BOX2)
"""
]

def create_prompt(inputs,num_prompts=8,method='random',seed=42,group=0):
    if method=='all':
        prompt_examples = OBJQUERY_CURATED_EXAMPLES
    elif method=='random':
        random.seed(seed)
        prompt_examples = random.sample(OBJQUERY_CURATED_EXAMPLES,num_prompts)
    else:
        raise NotImplementedError

    prompt_examples = '\n'.join(prompt_examples)
    prompt_examples = f'Think step by step to answer the question.\n\n{prompt_examples}'


    return prompt_examples + "\nQuestion: {question}\nProgram:".format(**inputs)