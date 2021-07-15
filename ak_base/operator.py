import json
from ak_base.modifiers import *
from ak_base.attack import Attack
from ak_base.calculation import *

class Operator (object):
    def __init__(self, src, skill_number):
        with open(src, encoding="utf8") as file:
            self._base = json.load(file)
        self.stats = self._base['stats'].copy()
        self.skill = self._base['skills'][skill_number - 1]
        self.skill['spData']['currentSp'] = self.skill['spData']['initSp']
        self.skill['active'] = False
        self.skill['delta'] = 0

        # ! Condense
        self.mods = mod_dict
        self.buffs = buff_list
        self.attack_mod = Attack()
        self.DoAttack = lambda enemy: PhysicalAttack(self, enemy)

    def AddBuff(self, *buffs):
        for buff in buffs:
            if buff not in self.buffs:self.buffs.append(buff)
            buff.on()

    def RemoveBuff (self, buff):
        if buff in self.buffs: self.buffs.remove(buff)
        buff.off()

    def AddAttack(self, bb):
        self.attack_mod.AddBlackboard(bb)

    def ResetAttack(self):
        self.attack_mod.Reset()

    def SetAttackFormula(self, formula):
        self.DoAttack = formula

    def _doPotential(self):
        for buff in self._base['potential']:
            self.AddBuff(Buff(f"Potential: {buff}", -1, buff, "add", self._base['potential'][buff]))
    
    def _doTrust(self):
        for buff in self._base['trust']:
            self.AddBuff(Buff(f"Trust: {buff}", -1, buff, "add", self._base['trust'][buff]))

if __name__ == "__main__":
    test = Operator("./parsed_src/op_src/char_103_angel.json", 1)
    a = Buff("buffA", 0, "atk", "mult", 5) # Test solo
    b = Buff("buffB", 0, "atk", "mult", 10) # Test stack
    c = Buff("buffC", 0, "atk", "add", 10) # Test order
    d = Buff("buffD", 0, "def", "add", 10) # Test type
    test.AddBuff(a,b,c,d)
    print(test.mods.getModifiers())
    # print([str(i) for i in test.mods["atk"]['add']])
    # print([i for i in test.buffs])