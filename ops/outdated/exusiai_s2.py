import json
# Base Relevant Content
op = {}
with open('../parsed_src/op_src/char_103_angel.json', 'r') as file: op = json.load(file)

# Buffs (Potential)
for buff in op['potential']:
    op['stats'][buff] += op['potential'][buff]

# Buffs (Trust)
for buff in op['trust']:
    op['stats'][buff] += op['trust'][buff]

# Buffs (Talent) - should be proceeded using manual discretion
op['stats']['atk'] = round(op['stats']['atk'] * 1.08, 2)
op['stats']['atkSpd'] += 15

# Resultant
op['stats']['atk/s'] = (op['stats']['atkSpd'] / op['stats']['atkTime']) / 100  # 1.15
# Consequentials
op['stats']['atkTime'] = round(1 / op['stats']['atk/s'], 2)

skill = op['skills'][1]
stats = op['stats']

# Configuration Conditions
enemy_def = 50
period = 60
timeline = [{
    'time': 0,
    'cDmg': 0,
    'total': 0,
    'currentSp': skill['spData']['initSp'],
    'isSkill': 0
}]

while timeline[-1]['time'] <= period:
    ref = timeline[-1]