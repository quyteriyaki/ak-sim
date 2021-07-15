from collections import defaultdict

a = defaultdict(lambda: None)

class Attack(defaultdict):
    def __init__(self, *args, **kwargs):
        if args: 
            super().__init__(*args, **kwargs)
        else: super().__init__(lambda: None)

    def AddBlackboard(self, blackboard):
        for key, value in blackboard.items():
            if key.startswith("attack@"):
                self[key] = value

    def Reset(self):
        for key,_ in self.items():
            del self[key]

if __name__ == "__main__":
    test_bb = {
        "times": 10,
        "attack@times": 5,
        "attack@atk_scale": 1.4
    }
    test = Attack()
    test.AddBlackboard(test_bb)

    print(test.items())