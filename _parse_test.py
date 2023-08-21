from engine import step_interpreters as si

STEP_STR1 = "OBJ1=SELECT(image=IMAGE,object=OBJ0,query='man in black henley',category=None)"
STEP_STR2 = "BOX1=SORT(box=BOX0,key='lambda x: x[0]',reverse=False)"
STEP_STR3 = '''OBJ2=SORT(obj=OBJ0,key="lambda x: x['box'][0]",reverse=True)'''

parse_result = si.parse_step(STEP_STR3)
print(parse_result)
