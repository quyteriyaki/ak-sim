from ak_base.operator import operator
from ak_base.simulate import simulation
import json


def main(skillNumber):
    op = operator("parsed_src/op_src/char_103_angel.json", skillNumber)
    # Buffs (Talent) - should be proceeded using manual discretion
    op.applyBuff('atk_%', 0.08)
    op.applyBuff('atkSpd', 15)

    # Skill
    def S1_On():
        op.applyAttack('atk_scale', 1.45)
        op.applyAttack('times', 3)
    
    def S1_Off():
        op.resetAttack('atk_scale')
        op.resetAttack('times')
    
    def S2_On():
        op.applyAttack('atk_scale', 1.25)
        op.applyAttack('times', 4)
    
    def S2_Off():
        op.resetAttack('atk_scale')
        op.resetAttack('times')
    
    def S3_On():
        op.applyAttack('atk_scale', 1.45)
        op.applyAttack('times', 5)
        op.applyBuff('atkTime', -0.22)
    
    def S3_Off():
        op.resetAttack('atk_scale')
        op.resetAttack('times')
        op.removeBuff('atkTime', -0.22)

    # Configuration Conditions
    # enemy_def = 50
    conf = {
        'period': 60,
        'enemy_def': 50,
        'trigger_type': "Instant",
        "atk_type": "Physical"
    }

    if skillNumber == 1:
        op.skill['skill_on'] = S1_On
        op.skill['skill_off'] = S1_Off
        conf['trigger_type'] = "Next"
    elif skillNumber == 2:
        op.skill['skill_on'] = S2_On
        op.skill['skill_off'] = S2_Off
    elif skillNumber == 3:
        op.skill['skill_on'] = S3_On
        op.skill['skill_off'] = S3_Off
    
    sim = simulation(op, conf)
    results = sim.run()
    total = 0
    for keys in results.keys:
        if "Attack" in keys[1]:
            print("{:.2f}".format(keys[0]), keys[1], results.data[keys[0]])
            if results.data[keys[0]] != []:
                total += results.data[keys[0]][1]
    print(round(total, 2))

if __name__ == "__main__":
    main(1) 