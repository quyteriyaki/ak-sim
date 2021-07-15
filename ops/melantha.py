from ak_base.operator import Operator, Buff
from ak_base.simulate import simulation
from ak_base.Timeline import Event
from ak_base.Events import *
import json
import sys

def main(skillNumber):
    op = Operator("parsed_src/op_src/char_208_melan.json", skillNumber)

    def S1_On(self):
        bb = op.skill['blackboard']
        self.S1_buff = Buff(op.skill['name'], op.skill['duration'], 'atk', "add", bb['atk'])
        op.AddBuff(self.S1_buff)

    def S1_Off(self):
        op.RemoveBuff(self.S1_buff)

    conf = {
        'period': 60,
        'enemy_def': 50,
        'trigger_type': "Instant",
        "atk_type": "Physical"
    }

    op.DoTick = Event("SPTick", 
        lambda op, t: spRec_Auto(op, t)
    )

    if skillNumber == 1:
        op.skill['on'] = S1_On
        op.skill['off'] = S1_Off

    sim = simulation(op, conf)
    results = sim.run()
    total = 0
    for key in results.keys:
        if "Attack" in results[key]:
            print("{:.2f}".format(key), [i for i in results[key]], results[key]["Attack"])
            if results[key]["Attack"] != None:
                total += results[key]["Attack"]
    print(round(total, 2))