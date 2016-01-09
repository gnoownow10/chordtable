from random      import randint
from random      import uniform
from functools   import partial
from functools   import reduce
from collections import namedtuple

def partials (p):
    return tuple((x + p) % 12 for x in [0, 7, 4, 10, 2])

def windex(l):
    total, cum = sum(l), 0
    n = uniform(0, total)
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

    @staticmethod
    def create(steps = 12, max_weight = 8):
        return Chordtable(
            weights=(0,) * steps,
            ages=(0,) * steps,
            steps=steps,
            max_weight=max_weight
        )

    def next_step(self):
        population = len([w for w in self.weights if w > 0])

        if population == 0:
            return randint(0, self.steps - 1), 1

        if windex([population, self.steps - population]) == 0:
            return self.choose_victim(), -1
        else:
            return self.choose_beneficiary(), 1

    def choose_beneficiary(self):
        classes     = range(0, self.steps)
        fundamental = windex([self.compute_power(p) for p in classes])

        harmonics   = partials(fundamental)
        weights     = (self.weights[p] for p in harmonics)
        rank_offset = len(harmonics) - 1
        rooms       = enumerate(self.max_weight - w for w in weights)

        i = windex([pow(2, rank_offset - rank) * room for rank, room in rooms])
        return harmonics[i]

    def compute_power(self, pitch_class, base=2):
        harmonics   = partials(pitch_class)
        rank_offset = len(harmonics) - 1
        weights     = enumerate(self.weights[p] for p in harmonics)
        return sum([w * pow(base, rank_offset - rank) for rank, w in weights])

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

        ages = (aging(w, a) for w, a in zip(self.weights, self.ages))
        return self._replace(weights=tuple(weights), ages=tuple(ages))
