import json

characters = {}
with open('./parsed_src/character_table.json', 'r') as file:
    characters = json.load(file)

skills = {}
with open('./parsed_src/skill_table.json', 'r') as file:
    skills = json.load(file)

for character in characters:
    with open('./parsed_src/op_src/'+character+'.json', 'w') as file:
        if 'skills' in characters[character]:
            list_skills = characters[character]['skills']
            characters[character]['skills'] = []
            for skill in list_skills:
                if str(skill) in skills:
                    characters[character]['skills'].append(skills[skill])
        file.write(json.dumps(characters[character], indent=2))