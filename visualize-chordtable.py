import chordtable

c = chordtable.Chordtable()

colors = ['#fff', '#fdd', '#fbb', '#f99', '#f77' ,'#f55', '#f33', '#f11']
names  = ['c','c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#' ,'a', 'a#' ,'b']

print '<style>td {width: 2em; height: 2em; text-align: center}</style>'
print '<table>'

for i in range(0, 1000):
    c.next()
    print '<tr>'
    for p, weight in enumerate(c.weights):
        print '<td style="background: %s">%s</td>' % (colors[weight], names[p])
    print '</tr>'
print '</table>'
