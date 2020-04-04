import json

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
            'trait': Group['trait'],
            'stats': Group['phases'][-1]['attributesKeyFrames'][-1],
            'skills': Group['skills'],
            'talents': Group['talents'],
            'potential': Group['potentialRanks'],
            'favorKeyFrames': Group['favorKeyFrames']
        }
    }
    char_out[ID] = object[ID]

for op in char_in:
    Parse_Selective(op, char_in[op])

with open('./parsed_src/chatacter_table.json', "w") as file:
    file.write(json.dumps(char_out))