import random

MAX_WEIGHT = 7
OP_WEIGHT, OP_LIGHTEN = 1, 0

def partials (p):
    return [(x + p) % 12 for x in [0, 7, 4, 10, 2]]

def windex(l):
    total, cum = sum(l), 0
    n = random.uniform(0, total)
    for i, weight in enumerate(l):
        cum += weight
        if n < cum: break
    return i

class Chordtable:
    def __init__ (self):
        self.steps = 12
        self.weights, self.ages = [0] * self.steps, [0] * self.steps

    def __iter__ (self):
        return self

    def weight (self, p):
        if self.weights[p] < MAX_WEIGHT: self.weights[p] += 1

    def lighten (self, p):
        if self.weights[p] > 0: self.weights[p] -= 1

    def census (self):
        return len([w for w in self.weights if w > 0])

    def next (self):
        population = self.census()
        if population > 0:
            if windex([population, (self.steps - population) * 1.2]):
                choice, op = self.nourish(windex(self.weights)), OP_WEIGHT
            else:
                choice, op = (self.tyrannize(windex([
                                sum([self.weights[c] * pow(2, 4 - i)
                                  for i, c in enumerate(partials(p))])
                                    for p, w in enumerate(self.weights)])),
                              OP_LIGHTEN)
        else:
            choice, op = random.randint(0, self.steps - 1), OP_WEIGHT
            self.weight(choice)

        self.outdate()
        return choice, op

    def nourish (self, p):
        allies = partials(p)
        choice = allies[windex([pow(2, 4 - i) * (MAX_WEIGHT - self.weights[c])
                        for i, c in enumerate(allies)])]
        self.weight(choice)
        return choice

    def tyrannize (self, tyrant):
        subs = partials(tyrant)
        choice = windex(
            [(p not in subs) 
             * (MAX_WEIGHT - self.weights[p] + 1)
             * self.ages[p] 
                for p, w in enumerate(self.weights)])
        self.lighten(choice)
        return choice

    def outdate (self):
        for p, w in enumerate(self.weights):
            if w > 0:
                self.ages[p] += 1
            else:
                self.ages[p] = 0