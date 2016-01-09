import random
from functools import partial
from functools import reduce
from collections import namedtuple

def partials (p):
    return tuple((x + p) % 12 for x in [0, 7, 4, 10, 2])

def windex(l):
    total, cum = sum(l), 0
    n = random.uniform(0, total)
    for i, weight in enumerate(l):
        cum += weight
        if n < cum: break
    return i

def clip(lo, hi, x):
    return max(lo, min(hi, x))

def aging(weight, age):
    if weight > 0:
        return age + 1
    else:
        return 0

class Chordtable(namedtuple('Chordtable', [
    'weights',
    'ages',
    'max_weight',
    'steps'
])):
    __slots__ = ()
    def next_step(self):
        population = len([w for w in self.weights if w > 0])

        if population == 0:
            return random.randint(0, self.steps - 1), 1

        to_vivify     = max(self.steps - (population + 2), 0)
        not_to_vivify = self.compute_cacophony()

        if windex([not_to_vivify, to_vivify * 1.2]):
            return self.choose_beneficiary(), 1
        else:
            return self.choose_victim(), -1

    def choose_beneficiary(self):
        fundamental = windex(self.weights)
        harmonics   = partials(fundamental)

        weights = (self.weights[p] for p in harmonics)
        rooms   = (self.max_weight - w for w in weights)

        index = windex([pow(2, 4 - rank) * room for rank, room in enumerate(rooms)])
        return harmonics[index]

    def compute_cacophony(self):
        def fn(sum, pair):
            p, w = pair
            if w and self.weights[(p - 1) % self.steps]:
                return sum + 1
            else:
                return sum
        return reduce(fn, enumerate(self.weights), 0) * 2

    def compute_power(self, pitch_class):
        harmonics = partials(pitch_class)
        weights   = (self.weights[p] for p in harmonics)
        return sum([w * pow(2, 4 - rank) for rank, w in enumerate(weights)])

    def compute_nuisance(self, pitch_class):
        weight = self.weights[pitch_class]
        age    = self.ages[pitch_class]
        return (self.max_weight - weight + 1) * age

    def choose_victim(self):
        classes     = range(0, self.steps)
        fundamental = windex([self.compute_power(p) for p in classes])
        inharmonics = tuple(p for p in classes if p not in partials(fundamental))

        return inharmonics[windex([self.compute_nuisance(i) for i in inharmonics])]

    def modify(self, *edits):
        weights = list(self.weights)
        for p, delta in edits:
            weights[p] = clip(0, self.max_weight, weights[p] + delta)

        pairs = zip(self.weights, self.ages)
        ages  = (aging(w, a) for w, a in pairs)
        return self._replace(weights=tuple(weights), ages=tuple(ages))

def create(steps = 12, max_weight = 7):
    return Chordtable(
        weights=(0,) * steps,
        ages=(0,) * steps,
        steps=steps,
        max_weight=max_weight
    )
