import json
flat = ['cost','sora_total', 'atk', 'def', 'maxHp', 'res', 'block', 'atkSpd', 'atkTime', 'hpRec', 'spRec', 'times']

class operator ():
    def __init__ (self, src, skill_number):
        with open(src, encoding="utf8") as file:
            self._op = json.load(file)
            self.stats = self._op['stats'].copy()
            self.skill = self._op['skills'][skill_number - 1]
            self.mods = {
                # Percentage Values
                'atk_%': 1,
                'def_%': 1,
                'maxHp_%': 1,
                'res_%': 1,
            }
            self.attack = {
                'atk_scale': 1, # Percentage
                'atk_to_hp_recovery_ratio': 0, # Sora S1 Specific, Float
                'buff_prob': 0, # Chance, Percentage
                'duration': 0, # Shirayuki Slow, Integer
                'frozen_duration': 0, # Frostleaf Slow, Integer
                'heal_scale': 1, # Saria + Nightmare heal, Percentage
                'interval': 0, # Magallan, Integer
                'max_target': 1, # Multi Target skill, Integer
                'move_speed': 0, # Shirayuki slow, Percentage
                'range_scale': 1, # Catapult nuke size, Percentage
                'sluggish': 0, # Magallan stop, Integer
                'times': 1 # Exu / BP Hits per attack, Integer
            }
            for buff in flat: self.mods[buff] = 0

            self._doPotential()
            self._doTrust()

    def applyBuff(self, name, val):
        if name not in self.mods:
            self.mods[name] = 1
        self._editBuff(name, val)

    def _editBuff(self, name, val):
        # Flat change
        if name in flat: self.mods[name] += val
        # probably will be Multiplicative
        else: self.mods[name] *= (val + 1)
        self._calculate()
    
    def removeBuff(self, name, val):
        if name in self.mods:
            self._editBuff(name, -val)

    def applyAttack(self, name, val):
        if name in self.attack:
            self.attack[name] = val

    def resetAttack(self, name):
        if name in self.attack:
            defaults = ['atk_scale', 'heal_scale', 'max_target', 'range_scale', 'times']
            if name in defaults:
                self.attack[name] = 1
            else: self.attack[name] = 0
                
    def _doPotential(self):
        for buff in self._op['potential']:
            self.applyBuff(buff, self._op['potential'][buff])
    
    def _doTrust(self):
        for buff in self._op['trust']:
            self.applyBuff(buff, self._op['trust'][buff])

    def _calculate (self):
        # Attack buffs 
        self.stats['atk'] = (self._op['stats']['atk'] + self.mods['atk']) * self.mods['atk_%']
        # Defense buffs
        self.stats['def'] = (self._op['stats']['def'] + self.mods['def']) * self.mods['def_%']
        # Max HP buffs
        self.stats['maxHp'] = (self._op['stats']['maxHp'] + self.mods['maxHp']) * self.mods['maxHp_%']
        # Res buffs
        self.stats['res'] = (self._op['stats']['res'] + self.mods['res']) * self.mods['res_%']
        # Attack speed buffs
        self.stats['atkSpd'] = self._op['stats']['atkSpd'] + self.mods['atkSpd']
        self.stats['atkTime'] = self._op['stats']['atkTime'] + self.mods['atkTime']
        # Attack speed application
        self.stats['atk/s'] = round((self.stats['atkSpd'] / self.stats['atkTime']) / 100, 2)
        self.stats['atkTime'] = round(1 / self.stats['atk/s'], 2)
        # HP / SP regen
        self.stats['hpRec'] = self._op['stats']['hpRec'] + self.mods['hpRec']
        self.stats['spRec'] = self._op['stats']['spRec'] + self.mods['spRec']
