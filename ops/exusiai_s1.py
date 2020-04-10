from ak_base.operator import operator
from ak_base.simulate import simulate
import json
op = operator("parsed_src/op_src/char_103_angel.json", 1)

def main():
    # Buffs (Talent) - should be proceeded using manual discretion
    op.applyBuff('atk', 1.08)
    op.applyBuff('atkSpd', 15)

    # Skill
    def Skill_On():
        return
    
    def Skill_Off():
        return
    # Configuration Conditions
    # enemy_def = 50
    conf = {
        'period': 60,
        'enemy_def': 50,
        'trigger_type': "Next",
        'skill_on': Skill_On,
        'skill_off': Skill_Off
    }

    sim = simulate(op, conf)
    results = sim.run()
    for keys in results:
        if "Attack" in keys[1]:
            print("{:.2f}".format(keys[0]), keys[1])

if __name__ == '__main__':
    main()