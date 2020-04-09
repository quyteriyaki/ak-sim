from ak_base.operator import operator
from tools.Timeline import Timeline
import json

t = Timeline()
op = operator("parsed_src/op_src/char_103_angel.json", 1)

def main():
    # Buffs (Talent) - should be proceeded using manual discretion
    op.applyBuff('atk', 1.08)
    op.applyBuff('atkSpd', 15)

    # Configuration Conditions
    # enemy_def = 50
    period = 60

    # Mark milestone
    t.addKey(0, "Init")
    currentSp = op.skill['spData']['initSp']
    ref = t.latest

    while ref[0] < period:
        current_time = ref[0]

        if "Attack" in ref[1] or "Init" in ref[1]:
            currentSp += 1
            if "SkillPrep" in ref[1]:
                currentSp = 0
                t.addKey(current_time + op.stats['atkTime'], "Skill")
            elif currentSp == op.skill['spData']['spCost']:
                t.addKey(current_time + op.stats['atkTime'], "SkillPrep")
            t.addKey(current_time + op.stats['atkTime'], "Attack")

        ref = t.getNext(current_time)

    for keys in t.keys:
        print("{:.2f}".format(keys[0]), keys[1])

if __name__ =='__main__':
    main()