import json

class operator ():
    def __init__ (self, src, skill_number):
        with open(src, encoding="utf8") as file:
            self._op = json.load(file)
            self.stats = self._op['stats'].copy()
            self.skill = self._op['skills'][skill_number - 1]
            self.mods = {}
            self._doPotential()
            self._doTrust()

    def applyBuff(self, name, val):
        if name not in self.mods:
            self.mods[name] = val
        else:
            self.mods[name] += val   
        self._calculate()

    def _doPotential(self):
        for buff in self._op['potential']:
            self.applyBuff(buff, self._op['potential'][buff])
    
    def _doTrust(self):
        for buff in self._op['trust']:
            self.applyBuff(buff, self._op['trust'][buff])
    
    def _calcSpeed(self):
        self.stats['atk/s'] = round((self.stats['atkSpd'] / self.stats['atkTime']) / 100, 2)
        self.stats['atkTime'] = round(1 / self.stats['atk/s'], 2)

    def _calculate (self):
        for buff in self.mods:
            self.stats[buff] = self._op['stats'][buff] + self.mods[buff]
        self._calcSpeed()
