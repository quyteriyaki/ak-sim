class Timeline:
    def __init__ (self):
        self.keys = []
    
    def add(self, e):
        self.keys.append(e)
    
    def remove(self, e):
        i = self.keys.index(e)
        return self.keys.pop(i)

def Key(time, cmd):
    return {
        time: cmd
    }

timeLine = Timeline()
timeLine.add(Key(100, "Attack"))
timeLine.add(Key(250, "Attack"))
timeLine.add(Key(160, "Attack"))
timeLine.add(Key(300, "Attack"))
timeLine.add(Key(110, "Attack"))

_t = sorted(timeLine.keys, key=lambda item: item.keys[0])
for key in timeLine.keys:
    print(key)