import json
import re
import bb_Repair

skills = {}
with open('./src/skill_table.json', 'r') as file:
    skills = json.load(file)

def Low_Skill_Removal(Group):
    # while len(Group['levels']) > 1:
    #     Group['levels'].pop(0)
    Group['levels'] = Group['levels'][-1]

def Name_Repair(Group):
    name = Group['levels']['name']
    if 'Î±' in name:
        Group['levels']['name'] = name.replace('Î±', 'α')
    if 'Î²' in name:
        Group['levels']['name'] = name.replace('Î²', 'β')
    if 'Î³' in name:
        Group['levels']['name'] = name.replace('Î³', 'γ')

def Parse_Desc(Group):
    desc = Group['levels']['description']
    bb = bb_Repair.toDict(Group['levels']['blackboard'])

    # Remove text formatting because we're not interested for the time being
    format_text_pat = "<.*?>"
    format_instances = re.findall(format_text_pat, desc)
    for term in format_instances: desc = desc.replace(term,"")
    
    # Translational issues due to special keys
    if "ï¼Œ" in desc: desc = desc.replace("ï¼Œ",", ")
    if "，" in desc: desc = desc.replace("，", ", ")
    if "â€™" in desc: desc = desc.replace("â€™","'")
    if "\u00e2\u20ac\u2122" in desc: desc = desc.replace("\u00e2\u20ac\u2122", "'")
    if "\u2019" in desc: desc = desc.replace("\u2019", "'")

    # Substitute Values
    sub_instances_pat = "{(.*?)}"
    sub_instances = re.findall(sub_instances_pat, desc)
    for key in sub_instances:
        old_key = "{" + key + "}"
        neg = False
        val = 0
        if "-" == key[0]:  # Test for negative
            # Effect: Values in data are negative, change to positive
            key = key[1:]
            neg = True
        
        if ':0.0%' in key: # Test for SilverAsh S2 [Rule of Survival] - dunno it just happens. No negative so we'll ignore
            # Effect: Maintain decimal + add percentage sign
            key = key[:-5]
            val = bb[key.lower()]
            val = str(val) + '%'
        elif ':0.0' in key: # Test for scale based fixed values
            # Effect: Maintain decimal
            key = key[:-4]
            val = bb[key.lower()]
            if neg: val *= -1
        elif ':0%' in key: # Test for percentage values
            # Multiply by 100 and add percentage sign
            key = key[:-3]
            val = round(bb[key.lower()] * 100)
            if neg: val *= -1
            val = str(val) + '%'
        else:
            val = bb[key.lower()]
            if neg: val *= -1
            val = str(int(val))
        desc = desc.replace(old_key, str(val))
    
    # Reconfigure skill
    # Reconfigure Blackboard to match dict
    Group['levels']['blackboard'] = bb
    # Return reference
    Group['levels']['description'] = desc
    skillId = Group['skillId']
    skills[skillId] = Group['levels']
    skills[skillId]['skillId'] = Group['skillId']
    # try:
    #     Group['levels']['description'] = desc.format(**bb)
    # except KeyError as e:
    #     if e.args[0][0] == '-':
    #         # Repair Negatives
    #         Group['levels']['description'] = -1 * e.args[0][1:]
    #     elif e.args[0].isupper() == True:
    #         # Repair Capitals
    #         Group['levels']['description'] = e.args[0].lower()
    #     elif '[' in e.args[0] or '.' in e.args[0]:
    #         # Repair symbols
    #     else:
    #        print(e.args[0])

for ID in skills:
    Low_Skill_Removal(skills[ID])
    Name_Repair(skills[ID])
    Parse_Desc(skills[ID])

with open('parsed_src/skill_table.json', 'w') as file:
    out = json.dumps(skills, indent=2)
    # Remove Blackboards
    # bb_pat = r'\, \"blackboard\": \[.*?\]'
    # bb_instance = re.findall(bb_pat, out)
    # for i in bb_instance:
    #     out = out.replace(i, "")
    file.write(out)