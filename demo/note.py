import random

class Note:
    def __init__ (self):
        self.pitch = 0
        self.params = [0, 0]

    def weight (self, pitch=60):
        if self.pitch == 0:
            self.pitch = pitch
        else:
            choices = [i for i, v in enumerate(self.params) if v < 10]
            if choices:
                self.params[random.choice(choices)] += 1

    def lighten (self):
        if not sum(self.params):
            self.pitch = 0
        else:
            choices = [i for i, v in enumerate(self.params) if v > 0]
            self.params[random.choice(choices)] -= 1

    def pitch_class (self):
        return self.pitch % 12

    def __repr__(self):
        return repr(tuple([self.pitch, ] + self.params))