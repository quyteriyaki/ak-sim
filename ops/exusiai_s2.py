from ak_base.operator import operator
from ak_base.simulate import simulate
import json
op = operator("parsed_src/op_src/char_103_angel.json", 2)

def main():
    # Buffs (Talent) - should be proceeded using manual discretion
    op.applyBuff('atk', 1.08)
    op.applyBuff('atkSpd', 15)

    # Configuration Conditions
    # enemy_def = 50
    conf = {
        'period': 60,
        'enemy_def': 50,
        'trigger_type': "Instant" 
    }
    
    sim = simulate(op, conf)
    results = sim.run()
    for keys in results:
        if "Attack" in keys[1]:
            print("{:.2f}".format(keys[0]), keys[1])

if __name__ == '__main__':
    main()