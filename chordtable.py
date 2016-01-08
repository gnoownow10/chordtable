import random
from functools import partial
from collections import namedtuple

Chordtable = namedtuple('Chordtable', [
    'weights',
    'ages',
    'max_weight',
    'steps'
])

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

def next_step(chordtable):
    population = len([w for w in chordtable.weights if w > 0])

    if population == 0:
        return random.randint(0, chordtable.steps - 1), 1

    to_vivify     = chordtable.steps - population
    not_to_vivify = population
    will_vivify   = windex([not_to_vivify, to_vivify * 1.2])

    if will_vivify:
        return choose_beneficiary(chordtable), 1
    else:
        return choose_victim(chordtable), -1

def choose_beneficiary(chordtable):
    fundamental = windex(chordtable.weights)
    harmonics   = partials(fundamental)

    weights = (chordtable.weights[p] for p in harmonics)
    rooms   = (chordtable.max_weight - w for w in weights)

    index = windex([pow(2, 4 - rank) * room for rank, room in enumerate(rooms)])
    return harmonics[index]

def compute_power(chordtable, pitch_class):
    harmonics = partials(pitch_class)
    weights   = (chordtable.weights[p] for p in harmonics)
    return sum([w * pow(2, 4 - rank) for rank, w in enumerate(weights)])

def compute_nuisance(chordtable, pitch_class):
    weight = chordtable.weights[pitch_class]
    age    = chordtable.ages[pitch_class]

    return (chordtable.max_weight - weight + 1) * age

def choose_victim(chordtable):
    power    = partial(compute_power, chordtable)
    nuisance = partial(compute_nuisance, chordtable)

    classes     = range(0, chordtable.steps)
    fundamental = windex([power(p) for p in classes])
    inharmonics = tuple(p for p in classes if p not in partials(fundamental))

    return inharmonics[windex([nuisance(i) for i in inharmonics])]

def modify(chordtable, *edits):
    weights = list(chordtable.weights)
    for p, delta in edits:
        weights[p] = clip(0, chordtable.max_weight, weights[p] + delta)

    pairs = zip(chordtable.weights, chordtable.ages)
    ages  = (aging(w, a) for w, a in pairs)
    return chordtable._replace(weights=tuple(weights), ages=tuple(ages))

def create(steps = 12, max_weight = 7):
    return Chordtable(
        weights=(0,) * steps,
        ages=(0,) * steps,
        steps=steps,
        max_weight=max_weight
    )
