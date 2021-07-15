from collections import defaultdict

class Timeline(defaultdict):
    def __init__(self, *args, **kwargs):
        if args: super().__init__(*args, **kwargs)
        else: super().__init__(lambda: defaultdict(lambda: 0))

    @property
    def keys(self):
        return sorted([i for i in self])

    @property
    def tail(self):
        return self.keys[-1], self[self.keys[-1]]
    
    def addKey(self, time, *cmds):
        time = round(time,2)
        for cmd in cmds:
            self[time][cmd]
    
    def moveKey(self, time, nTime):
        for cmd in self[time]:
            self.addKey(nTime, cmd)
        self.removeKey(time)

    def removeKey(self, time): del self[time]
    
    def removeCmd(self, time, cmd):
        del self[time][cmd]
        if not self[time]: self.removeKey(time)

    def removeLastCmd(self, cmd):
        for time in reversed(self.keys):
            if cmd in self[time]:
                self.removeCmd(time, cmd)
                return
        return

    def getNextKey(self, time, step = 1):
        if time not in self.keys:
            for i in self.keys:
                if time < i:
                    time = i
                    break

        e = self.keys.index(time) + step
        if e >= len(self.keys): e -= 1
        time = self.keys[e]
        #! Indicator for last element
        return time, self[time]

    def getPrevKey(self, time, step = 1):
        if time not in self.keys:
            for i in reversed(self.keys):
                if time > i:
                    time = i
                    break

        e = self.keys.index(time) - step
        if e < 0: e += 1
        time = self.keys[e]
        #! Indicator for first element
        return time, self[time]
    
    def getNextCmd(self, time, cmd):
        e = self.keys.index(time) + 1
        for n_time in self.keys[e:]:
            if cmd in self[n_time]: return n_time, self[n_time]
        return 0,0
    
    def getPrevCmd(self, time, cmd):
        e = self.keys.index(time)
        for n_time in reversed(self.keys[:e]):
            if cmd in self[n_time]: return n_time, self[n_time]
        return 0,0

class Event(object):
    def __init__(self, name, callback):
        self.name = name
        self.callback = callback

    def __call__(self):
        self.callback()