from ak_base.operator import operator
from ak_base.simulate import simulation
import json
import sys

def main(skillNumber):
    op = operator("parsed_src/op_src/char_172_svrash.json", skillNumber)

    # force SA base
    op._op['stats']['atk'] *= 0.8

    op.addBuff('atk_%', 0.12)
    # op.applyBuff('redeploy', -0.12)
    
    def S1_On():
        op.addAttack('atk_scale', 2.9)
    
    def S1_Off():
        op.resetAttack('atk_scale')
    
    def S3_On():
        op.addBuff('atk_%', 2)
        op.addBuff('def_%', -0.7)
    
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
        op.skill['on'] = S1_On
        op.skill['off'] = S1_Off
        conf['trigger_type'] = "Next"
    elif skillNumber == 3:
        op.skill['on'] = S3_On
        op.skill['off'] = S3_Off
    
    sim = simulation(op, conf)
    results = sim.run()
    total = 0
    for key in results.keys:
        if "Attack" in results[key]:
            print("{:.2f}".format(key), [i for i in results[key]], results[key]["Attack"])
            if results[key]["Attack"] != None:
                total += results[key]["Attack"]
    print(round(total, 2))

if __name__ == "__main__":
    main(int(sys.argv[1])) 