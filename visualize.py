#!/usr/bin/env python3

from chordtable.chordtable import Chordtable
import chordtable.misc as misc

from sys import exit

chord = Chordtable()
names = ['c','c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#' ,'a', 'a#' ,'b']

print('<style>td {width: 2em; height: 2em; text-align: center}</style>')
print('<table>')
for i in range(0, 1000):
    chord = chord.modify(chord.next_step())
    print('<tr>')
    for p, w in enumerate(chord.weights):
        color = misc.get_color(chord.max_weight, w)
        print('<td style="background: %s">%s</td>' % (misc.format_color(*color), names[p]))
    print('</tr>')
print('</table>')
