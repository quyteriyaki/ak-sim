import json
import bb_Repair

char_in = {}
char_out = {}

with open("./src/character_table.json", "r", encoding='utf8') as file:
    char_in = json.load(file)

def Parse_Selective (ID, Group):
    object = {
        ID: {
            "name": Group['name'],
            # 'description': Group['description'],
            'rarity': Group['rarity'],
            'profession': Group['profession'],
            'potential': Group['potentialRanks']
        }
    }

    # Translate Profession
    profession = Group['profession']
    if profession == "PIONEER":
        object[ID]['profession'] = "Vanguard"
    elif profession == "WARRIOR":
        object[ID]['profession'] = "Guard"
    elif profession == "TANK":
        object[ID]['profession'] = "Defender"
    elif profession == "MEDIC":
        object[ID]['profession'] = "Medic"
    elif profession == "SNIPER":
        object[ID]['profession'] = "Sniper"
    elif profession == "CASTER":
        object[ID]['profession'] = "Caster"
    elif profession == "SUPPORT":
        object[ID]['profession'] = "Supporter"
    elif profession == "SPECIAL":
        object[ID]['profession'] = "Specialist"

    # Remove Unnecessary Skill Information
    if len(Group['skills']) > 0:
        object[ID]['skills'] = []
        for skill in Group['skills']:
            object[ID]['skills'].append(skill['skillId'])

    # Remove Unnecessary Stat Information
    stats = Group['phases'][-1]['attributesKeyFrames'][-1]['data']
    object[ID]['stats'] = {
        'level': Group['phases'][-1]['attributesKeyFrames'][-1]['level'],
        'maxHp': stats['maxHp'],
        'atk': stats['atk'],
        'def': stats['def'],
        'res': stats['magicResistance'],
        'cost': stats['cost'],
        'block': stats['blockCnt'],
        'atkSpd': stats['attackSpeed'],
        'atkTime': stats['baseAttackTime'],
        'hpRec': stats['hpRecoveryPerSec'],
        'spRecoveryPerSec': stats['spRecoveryPerSec'],
        'respawn': stats['respawnTime']
    }

    # Remove Unnecessary Talent Information
    talents = Group['talents']
    if talents != None:
        object[ID]['talents'] = []
        for t in talents:
            if t['candidates'] != None:
                _tf = t['candidates'][-1]
                talent = {
                    'name': _tf['name'],
                    'description': _tf['description'],
                    'blackboard': bb_Repair.toDict(_tf['blackboard'])
                }
                object[ID]['talents'].append(talent)

    # Remove Unnecessary Trait Information
    traits = Group['trait']
    if traits != None:
        if len(traits) > 0:
            object[ID]['trait'] = []
            object[ID]['trait'].append(bb_Repair.toDict(traits['candidates'][0]['blackboard']))

    # Remove Unnecessary Trust Information
    trust = Group['favorKeyFrames']
    if trust != None:
        trust = trust[-1]['data']
        _t = {}
        for stat in trust:
            if trust[stat] != 0:
                _t[stat] = trust[stat]
        object[ID]['trust'] = _t

    # Remove Unnecessary Potential Information
    potential = Group['potentialRanks']
    if len(potential) > 0:
        _p = []
        for p in potential:
            buff = {
                'description': p['description']
            }
            if p['type'] == 0: # Switch between attributeTypes
                a = p['buff']['attributes']['attributeModifiers'][0]
                if a['attributeType'] == 0:
                    buff['maxHp'] = a['value'] # Max HP
                elif a['attributeType'] == 1:
                    buff['atk'] = a['value']   # ATK
                elif a['attributeType'] == 2:
                    buff['def'] = a['value']   # DEF
                elif a['attributeType'] == 3:
                    buff['res'] = a['value']   # Res
                elif a['attributeType'] == 4:
                    buff['cost'] = a['value']  # DP Cost
                elif a['attributeType'] == 7:
                    buff['attackSpeed'] = a['value']   # ASPD
                elif a['attributeType'] == 21:
                    buff['respawn'] = a['value']   # Redeployment Time
            #elif p['type'] == 1:
            #     buff['']
            _p.append(buff)
        object[ID]['potential'] = _p

    char_out[ID] = object[ID]

for op in char_in:
    Parse_Selective(op, char_in[op])

with open('./parsed_src/chatacter_table.json', "w") as file:
    file.write(json.dumps(char_out))