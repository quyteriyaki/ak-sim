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
        else:
            return super().__getattribute__(name)