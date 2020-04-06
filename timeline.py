# Base Relevant Content
base = {
    'atkSpd': 100,
    'atkTime': 1.0,
    'atk': 657,
    'states': {
        'normal': True,
        'S1': False
    }
}

# Buffs
buffs = {
    'atk': 1.08,
    'aspd': 15
}

# After buffs
base['atk'] *= buffs['atk']
base['atkSpd'] += buffs['aspd']

# Resultant
base['atk/s'] = (base['atkSpd'] / base['atkTime']) / 100  # 1.15
# Consequentials
base['atkInt'] = round(1 / base['atk/s'], 2)

# S1 relevant content
# SP cost
spCost = 4
initSp = 0

# Modifiers
atk_scale = 1.45
times = 3  # (Direct replacement of next attack)
enemy_def = 50

# Configuration Conditions
period = 60
timeline = [{
    'time': 0,
    'cDmg': 0,
    'total': 0,
    'currentSp': initSp
}]

while timeline[-1]['time'] <= period:
    ref = timeline[-1]
    keyframe = {
        'time': round(timeline[-1]['time'] + base['atkInt'], 2),
        'events': {},
        'total': 0
    }
    if ref['currentSp'] == spCost:
        keyframe['currentSp'] = 0
        keyframe['events']['S1'] = ((base['atk'] * atk_scale) - enemy_def) * times
    else:
        keyframe['currentSp'] = ref['currentSp'] + 1
        keyframe['events']['base'] = base['atk'] - enemy_def

    elist = []

    for event in keyframe['events']:
        keyframe['total'] += round(keyframe['events'][event], 2)
        elist.append(event)
    
    keyframe['cDmg'] = round(ref['cDmg'] + keyframe['total'], 2)
    output = "{:.2f} {:.2f} {:.2f}".format(keyframe['time'], keyframe['cDmg'], keyframe['total'])
    print(output, elist)
    timeline.append(keyframe)
