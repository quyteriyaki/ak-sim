class Timeline:
    def __init__ (self):
        self._keys = {}
    
    def add(self, time, cmd):
        if time in self._keys:
            self._keys[time].append(cmd)
        else:
            self._keys[time] = []
            self._keys[time].append(cmd)
    
    def remove(self, time):
        if time in self._keys:
            del self._keys[time]
    
    def __getattribute__(self,name):
        if name == "keys":
            return sorted(self._keys.items(), key=lambda item: item[0])
        elif name == "head":
            if len(self._keys) > 0:
                return self.keys[0]
            else:
                return 0
        else:
            return super().__getattribute__(name)
    
    def getNext(self, time, step = 1):
        e = (time, self._keys[time])
        i = self.keys.index(e) + step
        return self.keys[i][0]
    
    def getPrev(self, time, step = 1):
        e = (time, self._keys[time])
        i = self.keys.index(e) - step
        return self.keys[i][0]
    
    def pushKey(self, time, step):
        if time in self._keys:
            v = self._keys[time]
            for x in v:
                self.add(time + step, x)
        del self._keys[time]
    
    def moveKey(self, time, nTime):
        if time in self._keys:
            v = self._keys[time]
            for x in v:
                self.add(nTime, x)
        del self._keys[time]