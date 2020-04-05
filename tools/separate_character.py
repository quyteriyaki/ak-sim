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
            for skill in characters[character]['skills']:
                if str(skill) in skills:
                    characters[character]['skills'].remove(skill)
                    characters[character]['skills'].append(skills[skill])
        file.write(json.dumps(characters[character]))