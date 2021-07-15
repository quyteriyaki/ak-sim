import json

enemies = {}
with open('./src/enemy_database.json', 'r', encoding='utf8') as file:
    enemies = json.load(file)['enemies']

def quickKey(key, item):
    if item['m_defined'] == False:
        return None
    else:
        return item['m_value']

def ParseEnemy(enemy):
    object = []
    for level in enemy['Value']:
        obj_level = {
            "name": quickKey('name', level['enemyData']['name']),
            # "description": quickKey('description', level['enemyData']['description']),
            "prefabKey": quickKey('prefabKey', level['enemyData']['prefabKey']),
            # "lifePointReduce": quickKey("lifePointReduce", level['enemyData']['lifePointReduce'])
        }
        object.append(obj_level)

    print(object)

for enemy in enemies:
    ParseEnemy(enemy)