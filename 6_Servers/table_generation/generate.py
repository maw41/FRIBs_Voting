import random
import os
import struct
import copy
from datetime import datetime

# 4 bits plus carry
# 3 fragment servers
STATES = 16
obfuscated_lut = {}
result_lut = {}

def buildG():
	g = [[1,0,0,1,1,0], [0,1,0,1,0,1], [0,0,1,0,1,1]]
	lk = []
	lk2 = {}
	lk_valid = []
	for i in range(64):
		lk.append(-1)
	for i in range(8):
		o = 0
		v = bin(i)[2:].zfill(3)
		for j in range(6):
			o = (o<<1) + (((int(v[0]) * g[0][j]) + (int(v[1]) * g[1][j]) + (int(v[2]) * g[2][j])) % 2)
		lk[o] = i	
		oo = bin(o)[2:].zfill(6)
		for j in range(6):
			tmpj = oo[j]
			oo = '%s?%s' % (oo[0:j], oo[j+1:6])
			lk2[oo] = i
			oo = '%s%s%s' % (oo[0:j], tmpj, oo[j+1:6])
	lk_valid = copy.deepcopy(lk)
	for i in range(64):
		if lk[i] != -1:
			continue
		oo = bin(i)[2:].zfill(6)
		for j in range(6):
			tmpj = oo[j]
			oo = '%s?%s' % (oo[0:j], oo[j+1:6])
			if oo in lk2:
				lk[i] = lk2[oo]
				break
			oo = '%s%s%s' % (oo[0:j], tmpj, oo[j+1:6])
	return lk, lk_valid

lookupG, validG = buildG()

validResults = {}

def processValidResult(states):
	r = []
	v = 0
	c = 0

	# Decode block code
	iand = 1
	value = 0
	for i in range(4):
		b = 0
		for j in range(6):
			b = (b << 1) + ((states[j] & iand) >> i)
		if validG[b] == -1:
			return None
		else:
			vgb = validG[b]
			value = value << 1
			if vgb == 1 or vgb == 2 or vgb == 4 or vgb == 7:
				value += 1
		iand = iand << 1

	c = value & 1
	v = (value & 14) >> 1
	v += c
	rv = 0
	r2 = []
	for i in range(2):
		r2.append(random.randint(0,15))
		rv = rv ^ r2[i]
	r2.append(rv ^ v)

	for i in range(6):
		r.append(0)
		
	iand = 1
	for i in range(4):
		b = 0
		for j in range(3):
			b = (b << 1) + ((r2[j] & iand) >> i)
		b2 = validG.index(b) 
		band = 32
		for j in range(6):
			r[j] = (r[j] << 1) + ((b2 & band) >> (5-j))
			band = band >> 1	
		iand = iand << 1

	#for i in range(6):
	#	hr = bin(r[i])[2:].zfill(4)
	#	r[i] = int(hr[3]+hr[2]+hr[1]+hr[0],2)

	validResults[str(states)] = r

	for i in range(6):
		tmp = states[i]
		states[i] = -1
		validResults[str(states)] = r
		states[i] = tmp
	return None


def getResult(states):
	r = []
	v = 0
	c = 0

	if str(states) in validResults:
		return validResults[str(states)]

	for i in range(6):
		tmp = states[i]
		states[i] = -1
		if str(states) in validResults:
			return validResults[str(states)]
		states[i] = tmp
	# Only one server can be corrupt
	return None

for l in ['a', 'b', 'c', 'd', 'e', 'f']:
	obfuscated_lut[l] = {}
	result_lut[l] = []

for f in obfuscated_lut:
	for l in obfuscated_lut:
		obfuscated_lut[f][l] = []
		for i in range(STATES):
			obfuscated_lut[f][l].append(i)
		random.shuffle(obfuscated_lut[f][l])



for i0 in range(STATES):
	for i1 in range(STATES):
		for i2 in range(STATES):
			for i3 in range(STATES):
				for i4 in range(STATES):
					for i5 in range(STATES):
						processValidResult([i0,i1,i2,i3,i4,i5])

fa0 = obfuscated_lut['a']['a']
fb0 = obfuscated_lut['b']['b']
fc0 = obfuscated_lut['c']['c']
fd0 = obfuscated_lut['d']['d']
fe0 = obfuscated_lut['e']['e']
ff0 = obfuscated_lut['f']['f']

fa1 = obfuscated_lut['b']['a']
fb1 = obfuscated_lut['c']['b']
fc1 = obfuscated_lut['d']['c']
fd1 = obfuscated_lut['e']['d']
fe1 = obfuscated_lut['f']['e']
ff1 = obfuscated_lut['a']['f']

fa2 = obfuscated_lut['c']['a']
fb2 = obfuscated_lut['d']['b']
fc2 = obfuscated_lut['e']['c']
fd2 = obfuscated_lut['f']['d']
fe2 = obfuscated_lut['a']['e']
ff2 = obfuscated_lut['b']['f']

fa3 = obfuscated_lut['d']['a']
fb3 = obfuscated_lut['e']['b']
fc3 = obfuscated_lut['f']['c']
fd3 = obfuscated_lut['a']['d']
fe3 = obfuscated_lut['b']['e']
ff3 = obfuscated_lut['c']['f']

fa4 = obfuscated_lut['e']['a']
fb4 = obfuscated_lut['f']['b']
fc4 = obfuscated_lut['a']['c']
fd4 = obfuscated_lut['b']['d']
fe4 = obfuscated_lut['c']['e']
ff4 = obfuscated_lut['d']['f']

fa5 = obfuscated_lut['f']['a']
fb5 = obfuscated_lut['a']['b']
fc5 = obfuscated_lut['b']['c']
fd5 = obfuscated_lut['c']['d']
fe5 = obfuscated_lut['d']['e']
ff5 = obfuscated_lut['e']['f']

for i in range(STATES*STATES*STATES*STATES*STATES*STATES):
	result_lut['a'].append(128)
	result_lut['b'].append(128)
	result_lut['c'].append(128)
	result_lut['d'].append(128)
	result_lut['e'].append(128)
	result_lut['f'].append(128)

def getResultIndex(f0,f1,f2,f3,f4,f5):
	return (STATES * STATES * STATES * STATES * STATES * f0) + (STATES * STATES * STATES * STATES * f1) + (STATES * STATES * STATES * f2) + (STATES * STATES * f3) + (STATES * f4) + f5 


for i0 in range(STATES):
	for i1 in range(STATES):
		for i2 in range(STATES):
			for i3 in range(STATES):
				for i4 in range(STATES):
					for i5 in range(STATES):
						result_frags = getResult([i0,i1,i2,i3,i4,i5])
						if result_frags == None:
							continue
						result_lut['a'][getResultIndex(fa0[i0], fa1[i1], fa2[i2], fa3[i3], fa4[i4], fa5[i5])] = result_frags[0]
						result_lut['b'][getResultIndex(fb0[i1], fb1[i2], fb2[i3], fb3[i4], fb4[i5], fb5[i0])] = result_frags[1]
						result_lut['c'][getResultIndex(fc0[i2], fc1[i3], fc2[i4], fc3[i5], fc4[i0], fc5[i1])] = result_frags[2]
						result_lut['d'][getResultIndex(fd0[i3], fd1[i4], fd2[i5], fd3[i0], fd4[i1], fd5[i2])] = result_frags[3]
						result_lut['e'][getResultIndex(fe0[i4], fe1[i5], fe2[i0], fe3[i1], fe4[i2], fe5[i3])] = result_frags[4]
						result_lut['f'][getResultIndex(ff0[i5], ff1[i0], ff2[i1], ff3[i2], ff4[i3], ff5[i4])] = result_frags[5]


outdir = "output/%s" % (str(datetime.now()))
os.makedirs(outdir)
for s in result_lut:
	os.makedirs("%s/server_%s" % (outdir, s))
	f = open("%s/server_%s/result.lut" % (outdir, s), 'wb')
	for i in result_lut[s]:
		p = struct.pack("<B", i)
		f.write(p)
	f.close()
	for lut in obfuscated_lut[s]:
		f = open("%s/server_%s/%s.olut" % (outdir, s, lut), 'wb')
		#f = open("%s/server_%s/%s.olut" % (outdir, s, chr((ord(lut) - ord(s)) + 97)), 'wb')
		for i in obfuscated_lut[s][lut]:
			p = struct.pack("<B", i)
			f.write(p)
		f.close()
