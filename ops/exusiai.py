from ak_base.operator import Operator, Buff
from ak_base.simulate import simulation
import json
import sys


def main(skillNumber):
    op = Operator("parsed_src/op_src/char_103_angel.json", skillNumber)
    # Buffs (Talent) - should be proceeded using manual discretion
    trait_atk = Buff("trait_atk", -1, "atk", "mult", 0.08)
    trait_atkSpd = Buff("trait_atkSpd", -1, "atkSpd", "add", 155)
    op.AddBuff(trait_atk, trait_atkSpd)
    
    # Skill
    def S1_On():
        op.AddAttack(op.skill["blackboard"])
    
    def S1_Off():
        op.ResetAttack()
    
    def S2_On():
        op.AddAttack('atk_scale', 1.25)
        op.AddAttack('times', 4)

    def S2_Off():
        op.ResetAttack('atk_scale')
        op.ResetAttack('times')
    
    def S3_On():
        op.AddAttack('atk_scale', 1.45)
        op.AddAttack('times', 5)
        op.AddBuff('atkTime', -0.22)
    
    def S3_Off():
        op.ResetAttack('atk_scale')
        op.ResetAttack('times')
        op.RemoveBuff('atkTime', -0.22)

    # Configuration Conditions
    # enemy_def = 50
    conf = {
        'period': 60,
        'enemy_def': 50,
        'trigger_type': "Instant",
        "atk_type": "Physical"
    }

    if skillNumber == 1:
        op.skill['on'] = S1_On
        op.skill['off'] = S1_Off
        conf['trigger_type'] = "Next"
    elif skillNumber == 2:
        op.skill['on'] = S2_On
        op.skill['off'] = S2_Off
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