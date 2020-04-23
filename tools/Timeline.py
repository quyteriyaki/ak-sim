class Timeline:
    def __init__ (self):
        self._keys = {}
        self.keys = []
        self._output = {} # Data will be in tuples
        self.data = {}
    
    # Operators
    def addKey(self, time, *cmds):
        _time = round(time, 2)
        if _time in self._keys:
            for cmd in cmds:
                if cmd not in self._keys[_time]: self._keys[_time].append(cmd)
        else:
            self._keys[_time] = []
            for cmd in cmds:
                self._keys[_time].append(cmd)
        self.addData(_time, [])
    
    def addData(self, time, data):
        if time in self._keys:
            if time not in self._output:
                self._output[time] = data
            else:
                self._output[time] += data

    def moveKey(self, time, nTime):
        if time in self._keys:
            v = self._keys[time]
            for x in v:
                self.addKey(nTime, x)
        del self._keys[time]

    def rmKey(self, time):
        if time in self._keys:
            del self._keys[time]
            if time in self._output:
                del self._output[time]

    def rmLastCmd(self, cmd):
        c = len(self._keys) - 1
        while c >= 0:
            if cmd in self.keys[c][1]:
                self._keys[self.keys[c][0]].remove(cmd)
                return 1
            c -= 1
        return 0

    def rmCmd(self, time, cmd):
        if time in self._keys:
            self._keys[time].remove(cmd)
            if self._keys[time] == []:
                self.remove(time)

    # Retrievers
    def __getattribute__(self,name):
        if name == "keys":
            return sorted(self._keys.items(), key=lambda item: item[0])
        elif name == "data":
            return self._output
        elif name == "latest":
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

    # KillCmd should be used if a command is scheduled AFTER skill activation.
    # This will remove the last scheduled command.
    # Commonly used in: Auto Attack, batteries.
    def killCmd(self, cmd, old_key, kill_range):
        i = self.getNextCmd(old_key, cmd)
        # If next isn't self and exists
        if i != self.latest and i != 0:
            if i[0] > old_key + kill_range:
                self.rmCmd(i[0], cmd)