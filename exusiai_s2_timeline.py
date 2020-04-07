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
t.add(0, "Init")
skill = op['skills'][1]
currentSp = skill['spData']['initSp']
# 10, ["S2_On"],
# 25, ["S2_Off"]

state = "normal"
ref = t.getLatest()
duration = 0

def killAtk(old_time, diff):
    i = t.getNextCmd(old_time, "Attack")
    if i != ref:
        if i[0] > old_time + diff:
            t.rmCmd(i[0], "Attack")

while ref[0] < period:
    current_time = ref[0]
    cmd = []

    # Every SP tick
    if "SP" in ref[1] or "Init" in ref[1]:
        currentSp += 1
        if currentSp == skill['spData']['spCost']:
            # Kill the next attack if it's after the trigger
            killAtk(current_time, op['stats']['spRec'])
            
            # Force timing for attack at SP regen
            t.add(current_time + op['stats']['spRec'], "Skill", "Attack")

            # Force parameters
            duration = skill['duration']
            state = "Skill"
        else:
            # Tick SP as normal
            t.add(current_time + op['stats']['spRec'], "SP")
    
    # Skill = duration ticker
    if "Skill" in ref[1]:
        duration -= 1
        if duration == 0:
            # Kill the next attack if it's after the trigger
            killAtk(current_time, 1)
            # Force timing for attack after 1 second
            t.add(current_time + 1, "SP", "Attack")
            
            # Force parameters
            currentSp = 0
            state == "Normal"
        else:
            t.add(current_time + 1, "Skill")

    if "Attack" in ref[1] or "Init" in ref[1]:
        if t.getNextCmd(current_time, "Attack") != 0:
            i = t.getNextCmd(current_time, "Attack")
            if i != ref:
                if i[0] > current_time + op['stats']['atkTime']:
                    t.add(current_time + op['stats']['atkTime'], "Attack")
        else:
            t.add(current_time + op['stats']['atkTime'], "Attack")
    ref = t.getNext(current_time)

for keys in t.keys:
    if "Attack" in keys[1]:
        print("{:.2f}".format(keys[0]), keys[1])