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

skill = op['skills'][0]
stats = op['stats']

# Configuration Conditions
enemy_def = 50
period = 60
timeline = [{
    'time': 0,
    'cDmg': 0,
    'total': 0,
    'currentSp': skill['spData']['initSp']
}]

while timeline[-1]['time'] <= period:
    ref = timeline[-1]
    keyframe = {
        'time': round(timeline[-1]['time'] + stats['atkTime'], 2),
        'events': {},
        'total': 0
    }
    if ref['currentSp'] == skill['spData']['spCost']:
        keyframe['currentSp'] = 0
        keyframe['events']['S1'] = ((stats['atk'] * skill['blackboard']['atk_scale']) - enemy_def) * skill['blackboard']['times']
    else:
        keyframe['currentSp'] = ref['currentSp'] + 1
        keyframe['events']['base'] = stats['atk'] - enemy_def

    elist = []

    for event in keyframe['events']:
        keyframe['total'] += round(keyframe['events'][event], 2)
        elist.append(event)
    
    keyframe['cDmg'] = round(ref['cDmg'] + keyframe['total'], 2)
    output = "{:.2f} {:.2f} {:.2f}".format(keyframe['time'], keyframe['cDmg'], keyframe['total'])
    print(output, elist)
    timeline.append(keyframe)