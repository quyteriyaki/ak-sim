import tools.Timeline as tl
import json

t = tl.Timeline()
op = {}
with open('./parsed_src/op_src/char_103_angel.json') as file: op = json.load(file)

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

# Configuration Conditions
enemy_def = 50
period = 60

# Mark milestone
t.addKey(0, "Init")
skill = op['skills'][0]
currentSp = skill['spData']['initSp']

state = "normal"
ref = t.getLatest()
duration = 0

while ref[0] < period:
    current_time = ref[0]

    if "Attack" in ref[1] or "Init" in ref[1]:
        currentSp += 1
        if "SkillPrep" in ref[1]:
            currentSp = 0
            t.addKey(current_time + op['stats']['atkTime'], "Skill")
        elif currentSp == skill['spData']['spCost']:
            t.addKey(current_time + op['stats']['atkTime'], "SkillPrep")
        t.addKey(current_time + op['stats']['atkTime'], "Attack")

    ref = t.getNext(current_time)

for keys in t.keys:
    print("{:.2f}".format(keys[0]), keys[1])