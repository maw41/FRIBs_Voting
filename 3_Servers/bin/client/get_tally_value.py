import sys
import re

print 'Please enter the outputs from the three fragment servers (a, b, c).'
fragments = []
for i in ('a','b','c'):
	print 'Fragment server %s:' % (i)
	chars = []
	c = 0
	while c != '\n':
		c = sys.stdin.read(1)
		chars.append(c)
	f =  ''.join(chars)
	f = re.sub(r"[^\d,]","",f)
	f = f.split(',')
	fragments.append(f)

final_tally = 0
for i in range(len(fragments[0])):
	tally = 0
	for f in fragments:
		tally = tally ^ int(f[i])
	final_tally += (tally << (4 * i))
print final_tally
