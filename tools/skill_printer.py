import json

skills = {}
passed = []

with open('./parsed_src/skill_table.json') as file:
    skills = json.load(file)

with open('./parsed_src/skills_list.csv', 'w', encoding='utf8') as file:
    file.write("Skill, Type, Activation Type, Regen Type\n")
    for skill in skills:
        skillType = skills[skill]['levels']['skillType']
        if skillType == 0:
            skillType = "Passive"
        elif skillType == 1:
            skillType = "Manual"
        elif skillType == 2:
            skillType = "Auto"

        spType = skills[skill]['levels']['spData']['spType']
        if spType == 1:
            spType = "Auto Recovery"
        elif spType == 2:
            spType = "Offensive Recovery"
        elif spType == 4:
            spType = "Defensive Recovery"
        elif spType == 8:
            spType = "None"
        
        if skills[skill]['levels']['name'] not in passed:
             file.write(skills[skill]['levels']['name'] + ", ," + skillType + ", " + spType + "\n")
             passed.append(skills[skill]['levels']['name'])