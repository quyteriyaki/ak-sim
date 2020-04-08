class Timeline:
    def __init__ (self):
        self._keys = {}
    
    def addKey(self, time, *cmds):
        if time in self._keys:
            for cmd in cmds:
                if cmd not in self._keys[time]: self._keys[time].append(cmd)
        else:
            self._keys[time] = []
            for cmd in cmds:
                self._keys[time].append(cmd)
    
    def rmKey(self, time):
        if time in self._keys:
            del self._keys[time]
    
    def __getattribute__(self,name):
        if name == "keys":
            return sorted(self._keys.items(), key=lambda item: item[0])
        if name == "latest":
            return self.keys[-1]
        return super().__getattribute__(name)
    
    def getNext(self, time, step = 1):
        if time in self._keys:
            e = (time, self._keys[time])
            return self.keys[self.keys.index(e) + step]
        else:
            # Needs to be adjusted
            e = (0,self._keys[0])
            for i in self.keys:
                if e[0] - time < i[0] - time: e = i
                if e[0] - time > 0: break
            i = self.keys.index(e) + step - 1
            if i > len(self.keys) - 1:
                return self.keys[i - 1]
            return self.keys[i]
    
    def getPrev(self, time, step = 1):
        if time in self._keys:
            e = (time, self._keys[time])
            return self.keys[self.keys.index(e) - step]
        else:
            # Needs to be adjusted
            e = (0,self._keys[0])
            for i in self.keys:
                if time - e[0] < 0: break
                if time - e[0] > time - i[0] : e = i
            i = self.keys.index(e) - step
            if i > 0:
                return self.keys[0]
            return self.keys[i]       
    
    def moveKey(self, time, nTime):
        if time in self._keys:
            v = self._keys[time]
            for x in v:
                self.addKey(nTime, x)
        del self._keys[time]

    def rmLastCmd(self, cmd):
        c = len(self._keys) - 1
        while c >= 0:
            if cmd in self.keys[c][1]:
                self._keys[self.keys[c][0]].remove(cmd)
                return 1
            c -= 1
        return 0
    
    def getNextCmd(self, time, cmd):
        if time in self._keys:
            v = self.keys.index((time,self._keys[time])) + 1
            while v < len(self._keys):
                if cmd in self.keys[v][1]:
                    return self.keys[v]
                v += 1
        return 0
    
    def getPrevCmd(self, time, cmd):
        if time in self._keys:
            v = self.keys.index((time,self._keys[time])) - 1
            while  v > 0:
                if cmd in self.keys[v][1]:
                    return self.keys[v]
                v -= 1
        return 0
    
    def rmCmd(self, time, cmd):
        if time in self._keys:
            self._keys[time].remove(cmd)
            if self._keys[time] == []:
                self.remove(time)