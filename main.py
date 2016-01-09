import time
import sys

import composer
import chordtable

chord = chordtable.create()
great_composer = composer.Composer()

while True:
    p, delta = chord.next_step()
    for _ in range(0, 3):
        if delta == 1:
            great_composer.weight(p)
        elif delta == -1:
            great_composer.lighten(p)
    chord = chord.modify((p, delta))

    for beat in range(0, 24):
        for voice, staff in enumerate(great_composer.staves):
            print("{} {} {} {};".format(voice + 1,
                                       staff[beat].pitch,
                                       staff[beat].params[0],
                                       staff[beat].params[1]))
            sys.stdout.flush()
        time.sleep(0.125)
