from collections import defaultdict

class ModifierDict (defaultdict):
    def __init__(self, *args, **kwargs):
        if args: super().__init__(*args, **kwargs)
        else: super().__init__(lambda: defaultdict(lambda: []))

    def getModifiers(self):
        output = []
        for i in self.values():
            for j in i.values():
                output += [str(k) for k in j]
        return output

    def append(self, mod):
        self[mod.stat][mod.operand].append(mod)
    def remove(self, mod):
        self[mod.stat][mod.operand].remove(mod)

class BuffList (list):
    def __init__(self, *args, **kwargs):
        if args: super().__init__(*args, **kwargs)
        else: super().__init__(list())

    def __str__(self): return str([i.name for i in self])

mod_dict = ModifierDict()
buff_list = BuffList()

class Modifier (object):
    def __init__(self, name, stat, operand, value):
        global mod_dict
        self.mod_dict = mod_dict
        self.name = name
        self.stat = stat
        self.operand = operand
        self.value = value
        self.active = False
        # ? self.on()

    def __str__(self): 
        return f"{self.name} {self.stat} {self.operand} {self.value}"

    def on(self):
        if self.active: return
        self.mod_dict.append(self)
        self.active = True
        return self

    def off(self):
        if not self.active: return
        self.active = False
        self.mod_dict.remove(self)
        return self

class Buff (object):
    def __init__(self, name, duration, stat, operand, value):
        self.name = name
        self.duration = duration
        self.stat = stat
        self.operand = operand
        self.value = value
        self.active = False
        # Create timeline point forwhen buff will end
        self.modifier = Modifier(name, self.stat, self.operand, value)
    
    def on(self):
        global all_buffs
        if self.active: return
        self.active = True
        self.modifier.on()
    
    def off(self):
        global all_buffs
        if not self.active: return
        self.active = False
        self.modifier.off()

    def __str__(self):
        return f"{self.name} {self.stat} {self.operand} {self.value}"
