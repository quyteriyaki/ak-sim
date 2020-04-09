import tools.Timeline as tl
import json
from ak_base.operator import operator

t = tl.Timeline()
op = operator("parsed_src/op_src/char_103_angel.json", 3)

def killAtk(old_time, diff):
    i = t.getNextCmd(old_time, "Attack")
    if i != t.latest and i != 0:
        if i[0] > old_time + diff:
            t.rmCmd(i[0], "Attack")

def main():
    # Buffs (Talent) - should be proceeded using manual discretion
    op.applyBuff('atk', 1.08)
    op.applyBuff('atkSpd', 15)

    # Configuration Conditions
    enemy_def = 50
    period = 60

    # Mark milestone
    t.addKey(0, "Init")
    currentSp = op.skill['spData']['initSp']

    state = "normal"
    ref = t.latest
    duration = 0

    while ref[0] < period:
        current_time = ref[0]
        # Every SP tick
        if "SP" in ref[1] or "Init" in ref[1]:
            currentSp += 1
            if currentSp == op.skill['spData']['spCost']:
                # Kill the next attack if it's after the trigger
                killAtk(current_time, op.stats['spRec'])
            
                # Force timing for attack at SP regen
                t.addKey(current_time + op.stats['spRec'], "Skill", "Attack")

                # Force parameters
                duration = op.skill['duration']
                state = "Skill"
            
                # Force buffs
                op.applyBuff('atkTime', 0.22)
            else:
                # Tick SP as normal
                t.addKey(current_time + op.stats['spRec'], "SP")

        # Skill = duration ticker
        if "Skill" in ref[1]:
            duration -= 1
            if duration == 0:
                # Kill the next attack if it's after the trigger
                killAtk(current_time, 1)
                # Force timing for attack after 1 second
                t.addKey(current_time + 1, "SP", "Attack")

                # Force parameters
                currentSp = 0
                state == "Normal"

                # Force revert buffs
                op.applyBuff('atkTime', -0.22)
            else:
                t.addKey(current_time + 1, "Skill")

        if "Attack" in ref[1] or "Init" in ref[1]:
            if t.getNextCmd(current_time, "Attack") != 0:
                i = t.getNextCmd(current_time, "Attack")
                if i != ref:
                    if i[0] > current_time + op.stats['atkTime']:
                        t.addKey(current_time + op.stats['atkTime'], "Attack")
            else:
                t.addKey(current_time + op.stats['atkTime'], "Attack")
        ref = t.getNext(current_time)


    for keys in t.keys:
        if "Attack" in keys[1]:
            print("{:.2f}".format(keys[0]), keys[1])

if __name__ == '__main__':
    main()