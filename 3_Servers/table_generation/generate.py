import random, os, struct
from datetime import datetime

# 4 bits plus carry
# 3 fragment servers
STATES = 32
obfuscated_lut = {}
result_lut = {}

def getResult(args):
	r = []
	v = 0
	c = 0
	for arg in args:
		c = c ^ (arg & 1)
		v = v ^ (arg >> 1)
	v = v + c	
	rv = 0
	for i in range(len(args)-1):
		r.append(random.randint(0,31))
		rv = rv ^ r[i]
	r.append(rv ^ v)
	return r

for l in ["a", "b", "c"]:
	obfuscated_lut[l] = {}
	result_lut[l] = []

for f in obfuscated_lut:
	for l in obfuscated_lut:
		obfuscated_lut[f][l] = []
		for i in range(STATES):
			obfuscated_lut[f][l].append(i)
		random.shuffle(obfuscated_lut[f][l])

for f in result_lut:
	for i in range(STATES*STATES*STATES):
		result_lut[f].append(0)

fa0 = obfuscated_lut["a"]["a"]
fb0 = obfuscated_lut["b"]["b"]
fc0 = obfuscated_lut["c"]["c"]
fa1 = obfuscated_lut["b"]["a"]
fb1 = obfuscated_lut["c"]["b"]
fc1 = obfuscated_lut["a"]["c"]
fa2 = obfuscated_lut["c"]["a"]
fb2 = obfuscated_lut["a"]["b"]
fc2 = obfuscated_lut["b"]["c"]
for i0 in range(STATES):
	for i1 in range(STATES):
		for i2 in range(STATES):
			result_frags = getResult([i0,i1,i2])
			result_lut["a"][(STATES * STATES * fa0[i0]) + (STATES * fa1[i1]) + fa2[i2]] = result_frags[0]
			result_lut["b"][(STATES * STATES * fb0[i1]) + (STATES * fb1[i2]) + fb2[i0]] = result_frags[1]
			result_lut["c"][(STATES * STATES * fc0[i2]) + (STATES * fc1[i0]) + fc2[i1]] = result_frags[2] 

outdir = "output/%s" % (str(datetime.now()))
os.makedirs(outdir)
for s in result_lut:
	os.makedirs("%s/server_%s" % (outdir, s))
	f = open("%s/server_%s/result.lut" % (outdir, s), "wb")
	for i in result_lut[s]:
		p = struct.pack("<B", i)
		f.write(p)
	f.close()
	for lut in obfuscated_lut[s]:
		f = open("%s/server_%s/%s.olut" % (outdir, s, lut), "wb")
		for i in obfuscated_lut[s][lut]:
			p = struct.pack("<B", i)
			f.write(p)
		f.close()
