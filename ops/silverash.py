from ak_base.operator import operator
from ak_base.simulate import simulation
import json

def main(skillNumber):
    op = operator("parsed_src/op_src/char_172_svrash.json", skillNumber)

    # force SA base
    op._op['stats']['atk'] *= 0.8

    op.applyBuff('atk_%', 0.12)
    # op.applyBuff('redeploy', -0.12)
    
    def S1_On():
        op.applyAttack('atk_scale', 2.9)
    
    def S1_Off():
        op.resetAttack('atk_scale')
    
    def S3_On():
        op.applyBuff('atk_%', 2)
        op.applyBuff('def_%', -0.7)
    
    def S3_Off():
        op.removeBuff('atk_%', 2)
        op.removeBuff('atk_%', -0.7)

    conf = {
        'period': 60,
        'enemy_def': 50,
        'trigger_type': "Instant",
        'atk_type': "Physical"
    }

    if skillNumber == 1:
        op.skill['skill_on'] = S1_On
        op.skill['skill_off'] = S1_Off
        conf['trigger_type'] = "Next"
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