import time
import sys

import composer
import chordtable

inspiration = chordtable.Chordtable()
great_composer = composer.Composer()

for pitch_class, op in inspiration:
    for _ in range(0, 3):
        if op == chordtable.OP_WEIGHT:
            great_composer.weight(pitch_class)
        elif op == chordtable.OP_LIGHTEN:
            great_composer.lighten(pitch_class)

    for beat in range(0, 24):
        for voice, staff in enumerate(great_composer.staves):
            print "{} {} {} {};".format(voice + 1,
                                       staff[beat].pitch,
                                       staff[beat].params[0],
                                       staff[beat].params[1])
            sys.stdout.flush()
        time.sleep(0.125)
