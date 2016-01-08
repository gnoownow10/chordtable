import random
import note
from functools import reduce

allowed_leap = lambda steps: 24 - steps * 3
LEAP_TEST_RANGE = 4

class Composer:
    def __init__ (self, staves=4, beats=24):
        self.staves = [[note.Note() for _ in range(beats)] for _ in range(staves)]

    def weight (self, pitch_class):
        choices = []
        for voice, staff in enumerate(self.staves):
            for beat, note in enumerate(staff):
                if not note.pitch:
                    choices += [(pitch, voice, beat)
                        for pitch in map(lambda octs: octs * 12 + pitch_class,
                                         range(1, 6))
                        if self.is_sensible_leap(pitch, voice, beat)]

                elif note.pitch_class() == pitch_class:
                    choices += [(note.pitch, voice, beat)]

        if choices:
            pitch, voice, beat = random.choice(choices)
            self.staves[voice][beat].weight(pitch)

    def lighten (self, pitch_class):
        choices = [(voice, beat)
            for voice, staff in enumerate(self.staves)
                for beat, note in enumerate(staff)
                    if note.pitch and note.pitch_class() == pitch_class]
        if choices:
            voice, beat = random.choice(choices)
            self.staves[voice][beat].lighten()

    def is_sensible_leap (self, pitch, voice, beat):
        staff = self.staves[voice]
        return reduce(lambda result, step:
                        result and
                          ((staff[beat - step].pitch == 0) or
                           (allowed_leap(step) >
                            abs(pitch - staff[beat - step].pitch))), 
                      range(1, 1 + LEAP_TEST_RANGE), True)
