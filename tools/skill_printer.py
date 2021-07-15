import json

skills = {}
passed = []

with open('./parsed_src/skill_table.json', encoding="utf8") as file:
    skills = json.load(file)

def printSkillTypes():  
    with open('./notes/skills_list.csv', 'w', encoding='utf8') as file:
        file.write("Skill, Type, Activation Type, Regen Type, Duration\n")
        for skill in skills:
            skillType = skills[skill]['skillType']
            if skillType == 0:
                skillType = "Passive"
            elif skillType == 1:
                skillType = "Manual"
            elif skillType == 2:
                skillType = "Auto"

            spType = skills[skill]['spData']['spType']
            if spType == 1:
                spType = "Auto Recovery"
            elif spType == 2:
                spType = "Offensive Recovery"
            elif spType == 4:
                spType = "Defensive Recovery"
            elif spType == 8:
                spType = "None"
        
            if skills[skill]['name'] not in passed:
                 file.write(skills[skill]['name'] + ", ," + skillType + ", " + spType + ", " + str(skills[skill]['duration']) + "\n")
                 passed.append(skills[skill]['name'])

def printBuffs ():
    record = []
    with open('./notes/skill_buffs.csv', 'w') as file:   
        file.write("Buff name, Description, Additive / Multiplicative \n")
        for skill in skills:
            for buff in skills[skill]['blackboard']:
                if buff not in record:
                    record.append(buff)
                    file.write(buff + ", , \n")

printSkillTypes()