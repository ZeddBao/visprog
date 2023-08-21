import random

OBJQUERY_CURATED_EXAMPLES=[
"""Question:the yellow duck
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='yellow duck',category='bird')
FINAL_RESULT=RESULT(var=OBJ1)
"""
,
"""Question:the third cup from bottom
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='cup',category='cup')
OBJ2=SORT(object=OBJ1,key="lambda x: x['box'][3]",reverse=True)
OBJ3=INDEX(item=OBJ2,index=2)
FINAL_RESULT=RESULT(var=OBJ3)
"""
,
"""Question:the first duck from right
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='duck',category='bird')
OBJ2=SORT(object=OBJ1,key="lambda x: x['box'][2]",reverse=True)
OBJ3=INDEX(item=OBJ2,index=0)
FINAL_RESULT=RESULT(var=OBJ3)
"""
,
"""Question:the second person from top
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='person',category='person')
OBJ2=SORT(object=OBJ1,key="lambda x: x['box'][1]",reverse=False)
OBJ3=INDEX(item=OBJ2,index=1)
FINAL_RESULT=RESULT(var=OBJ3)
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