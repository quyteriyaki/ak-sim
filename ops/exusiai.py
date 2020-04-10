from ak_base.operator import operator
from ak_base.simulate import simulate
import json


def main(skillNumber):
    op = operator("parsed_src/op_src/char_103_angel.json", skillNumber)
    # Buffs (Talent) - should be proceeded using manual discretion
    op.applyBuff('atk_%', 0.08)
    op.applyBuff('atkSpd', 15)

    # Skill
    def S1_On():
        op.applyBuff('atk_scale', 1.45)
    
    def S1_Off():
        op.removeBuff('atk_scale', 1.45)
    
    def S2_On():
        op.applyAttack('attack@atk_scale', 1.25)
        op.applyAttack('attack@times', 4)
    
    def S2_Off():
        op.resetAttack('attack@atk_scale')
        op.resetAttack('attack@times')
    
    def S3_On():
        op.applyAttack('attack@atk_scale', 1.45)
        op.applyAttack('attack@times', 5)
        op.applyBuff('atkTime', -0.22)
    
    def S3_Off():
        op.resetAttack('attack@atk_scale')
        op.resetAttack('attack@times')
        op.removeBuff('atkTime', -0.22)

    # Configuration Conditions
    # enemy_def = 50
    conf = {
        'period': 60,
        'enemy_def': 50,
        'trigger_type': "Instant"
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
    
    sim = simulate(op, conf)
    results = sim.run()
    for keys in results:
        if "Attack" in keys[1]:
            print("{:.2f}".format(keys[0]), keys[1])
