import struct
import socket
import sys
from threading import Thread
import random
import copy #TEMP
from time import sleep #TEMP
from Queue import Queue
import time

STATES = 16

class Server:
	def loadResultLut(path):
		return 0

class RemoteServer(Server):
	def __init__(self, ip=None, seed=None, riport=None, rvport=None, iport=None, vport=None, label=None, scheduler_port=None):
		self.ip = ip
		self.riport = riport
		self.rvport = rvport
		self.iport = iport 
		self.vport = vport 
		self.isock = None
		self.iconn = None
		self.iaddr = None
		self.vsock = None
		self.vconn = None
		self.vaddr = None
		self.random = random.Random()
		self.random.seed(seed)
		self.label = label
		self.q = Queue()
		self.scheduler_port = scheduler_port

	def obfuscate(self, state):
		return self.olut[state]

	def connect(self):
		self.risock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.rvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.risock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		self.rvsock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		try:
			self.risock.connect((self.ip, self.riport)) 
			self.rvsock.connect((self.ip, self.rvport)) 
			print 'Connected.'
			return True
		except:
			return False	

	def stop(self):
		self.risock.close()
		self.rvsock.close()
	
	def loadLut(self, path):
		self.olut = []
		f = open(path, 'rb')
		while True:
			b = f.read(1)
			if not b: 
				break
			self.olut.append(b)
		f.close()

class LocalServer(Server):
	def __init__(self, remote_servers):
		self.a = remote_servers[0] 
		self.b = remote_servers[1] 
		self.c = remote_servers[2] 
		self.d = remote_servers[3] 
		self.e = remote_servers[4] 
		self.f = remote_servers[5] 
		self.voteaddQ = Queue()
		self.vectorBQ = Queue()

	def initiateTally(self, value, length):
		assert(length % 3 == 0)	
		self.tally_length = length
		self.tally = value

	def startListeningIndex(self, remote_server):
		remote_server.isock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		remote_server.isock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		remote_server.isock.bind(('0.0.0.0', remote_server.iport))
		remote_server.isock.listen(0)
		remote_server.iconn, remote_server.iaddr = remote_server.isock.accept() 
		print 'Listen Connected to %s' % remote_server.label

	def listeningIndex(self, remote_servers):
		# Should be: b,d,e,f
		lthreads = []
		for remote_server in [self.b, self.c, self.d, self.e, self.f]:
			lt = Thread(target=self.startListeningIndex, args=(remote_server,))
			lt.start()
			lthreads.append(lt)
		for lt in lthreads:
			lt.join()
		print 'All joined'	
		
		row_bytes_inorder = []
		#for k in range(STATES):
		#	row_bytes_inorder.append(k)
		for k in range(3):
			row_bytes_inorder.append(k)

		#states_x_pre = STATES * 4 * 4 
		states_x_pre = 3 * 3 * 3 
		while True:
			indexes = []
			for remote_server in remote_servers:
				b1 = remote_server.iconn.recv(1)
				if len(b1) == 0:
					return
				indexes.append(struct.unpack("<B", b1)[0])
			#osb = remote_servers[0].q.get()
			osb = self.vectorBQ.get()

			osbf = 0
			states_x = states_x_pre 
			oss = 0
			for i in [1,2,3]:
				oss += (states_x * indexes[i])	
				states_x = states_x / 3 

			i = 0
			osbf = 0
			osbi = 0
			while i < 3:
				#for j in range(STATES*STATES*STATES*STATES):
				#	row_bytes.append(j)
				#remote_servers[0].random.shuffle(row_bytes)
				#osb_new = row_bytes.index(osb)
				#osb_new = osb
				j = 0
				while j < 27:
					row_bytes = copy.deepcopy(row_bytes_inorder)
					remote_servers[0].random.shuffle(row_bytes)
					osb_new = row_bytes.index(osb) 
					k = 0	
					while k < 3:
						tmp_r = self.b.random.randint(0,STATES-1)
						if i == indexes[0] and j*3 == oss and k == osb_new:
							osbf = tmp_r
							osbi = osb_new + oss
							'''while k < STATES:
								self.b.random.randint(0,STATES-1)
								k += 1
							while j < 64:
								remote_servers[0].random.shuffle(row_bytes)
								k = 0	
								while k < STATES:
									self.b.random.randint(0,STATES-1)
									k += 1
								j += 1
							while i < 4:
								j = 0
								while j < 64:
									remote_servers[0].random.shuffle(row_bytes)
									k = 0	
									while k < STATES:
										self.b.random.randint(0,STATES-1)
										k += 1
									j += 1
								i += 1
							break'''
						k += 1
					j += 1
				i += 1
			remote_servers[0].iconn.sendall(struct.pack("<BB", osbi & 255, (osbi >> 8) & 255) + struct.pack("<B", (osbf & 255)))
		sleep(5)
		for remote_server in [self.b, self.c, self.d, self.e, self.f]:
			remote_server.iconn.close()
		print 'listeningIndex closing.'
		sys.exit()
		#thread.exit()

	def startListeningMiniLUT(self, remote_server):
		remote_server.vsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		remote_server.vsock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		remote_server.vsock.bind(('0.0.0.0', remote_server.vport))
		remote_server.vsock.listen(0)
		remote_server.vconn, remote_server.vaddr = remote_server.vsock.accept() 
		print 'listeningMiniLUT Connected to %s' % remote_server.label

	def listeningMiniLUT(self, remote_servers):
		#should be b,c,d,f in order f,b,c,d
		lthreads = []
		#for remote_server in remote_servers:
		for remote_server in [self.b, self.c, self.d, self.e, self.f]:
			lt = Thread(target=self.startListeningMiniLUT, args=(remote_server,))
			lt.start()
			lthreads.append(lt)
		for lt in lthreads:
			lt.join()
		print 'All joined'	


		STATES5 = STATES * STATES * STATES * STATES * STATES
		STATES4 = STATES * STATES * STATES * STATES
		STATES3 = STATES * STATES * STATES
		STATES2 = STATES * STATES

		while True:
			break_main = False 
			vectors = []
			#for remote_server in remote_servers:
			for remote_server in [self.f, self.b, self.c, self.d, self.e]:
				b4 = remote_server.vconn.recv(3)
				if len(b4) == 0:
					break_main = True
					break
				vectors.append(struct.unpack("<BBB", b4))
			if break_main:
				break
			osf = remote_servers[0].q.get() * STATES4
			rbs = ''
			j = 0
			prev = None
			for i0 in [0,1,2]:
				b0 = osf + (vectors[0][i0] * STATES5)
				for i1 in [0,1,2]:
					b1 = b0 + (vectors[1][i1] * STATES3)
					for i2 in [0,1,2]:
						b2 = b1 + (vectors[2][i2] * STATES2)
						for i3 in [0,1,2]:
							b3 = b2+ (vectors[3][i3] * STATES)
							row_bytes = [0,0,0]
							for i4 in [0,1,2]:
								i = b3 + (vectors[4][i4])
								row_bytes[i4] = self.result_lut[i] 
							self.f.random.shuffle(row_bytes)
								
							rb1 = row_bytes[0]
							rb2 = row_bytes[1]
							rb3 = row_bytes[2]
							tmp_r1 = self.f.random.randint(0,STATES-1)
							tmp_r2 = self.f.random.randint(0,STATES-1)
							tmp_r3 = self.f.random.randint(0,STATES-1)
							rbs += struct.pack("<B", (struct.unpack("<B", rb1)[0] ^ tmp_r1))
							rbs += struct.pack("<B", (struct.unpack("<B", rb2)[0] ^ tmp_r2))
							rbs += struct.pack("<B", (struct.unpack("<B", rb3)[0] ^ tmp_r3))

							continue
							#if j == 0:
							#	rb1 = row_bytes[j]
							#	rb2 = row_bytes[j+1]
							#	rb3 = row_bytes[j+2]
							#	tmp_r1 = self.f.random.randint(0,STATES-1)
							#	tmp_r2 = self.f.random.randint(0,STATES-1)
							#	tmp_r3 = self.f.random.randint(0,STATES-1)
							#	rbs += struct.pack("<B", (((struct.unpack("<B", rb1)[0] ^ tmp_r1) & 15 << 4) + ((struct.unpack("<B", rb2)[0] ^ tmp_r2) & 15)))
							#	prev =  ((struct.unpack("<B", rb1)[0] ^ tmp_r3) & 15 << 4) 
							#	j = 1
							#else:
							#	rb1 = row_bytes[0]
							#	rb2 = row_bytes[1]
							#	rb3 = row_bytes[2]
							#	tmp_r1 = self.f.random.randint(0,STATES-1)
							#	tmp_r2 = self.f.random.randint(0,STATES-1)
							#	tmp_r3 = self.f.random.randint(0,STATES-1)
							#	rbs += struct.pack("<B", (prev + ((struct.unpack("<B", rb2)[0] ^ tmp_r1) & 15)))
							#	rbs += struct.pack("<B", (((struct.unpack("<B", rb2)[0] ^ tmp_r1) & 15 << 4) + ((struct.unpack("<B", rb2)[0] ^ tmp_r3) & 15)))
							#	prev = None
							#	j = 0


			#print 'Lenght of rbs is %s' % len(rbs)
			#rbs = '0' * 123	
			remote_servers[0].vconn.sendall(rbs)
			
		sleep(5)
		for remote_server in [self.b, self.c, self.d, self.e, self.f]:
			remote_server.iconn.close()
		print 'listeningMiniLUT closing.'
		sys.exit()
		#thread.exit()
	def listen(self):
		self.lithread = Thread(target = self.listeningIndex, args = ([self.b, self.d, self.e, self.f],))
		self.mlthread = Thread(target = self.listeningMiniLUT, args = ([self.f, self.b, self.c, self.d],))
		self.avthread = Thread(target = self.addVote, args = ())
		self.lithread.start()
		self.mlthread.start()
		self.avthread.start()


	def loadResultLut(self, path):
		self.result_lut = []	
		f = open(path, 'rb')
		while True:
			b = f.read(1)
			if not b: 
				break
			self.result_lut.append(b)
		f.close()

	def parreduces(self, pstates):
		pvis = []
		for states in pstates:
			my_vis = []
			sends_rv = {}
			sends_ri = {}
			for remote_server in [self.b, self.c, self.d, self.e, self.f]:
				sends_rv[remote_server] = ""
				sends_ri[remote_server] = ""

			for state in states:
				osa = self.a.obfuscate(state)
				osb = self.b.obfuscate(state)
				osc = self.c.obfuscate(state)
				osd = self.d.obfuscate(state)
				ose = self.e.obfuscate(state)
				#for remote_server in [self.b, self.c, self.d, self.e, self.f]:
				for remote_server in [self.c, self.d, self.e, self.f]:
					remote_server.q.put(struct.unpack("<B", remote_server.obfuscate(state))[0])

				my_vi = -1
				for osx in [[osa, self.b, self.f], [osb, self.c, None], [osc, self.d, self.b], [osd, self.e, self.c], [ose, self.f, self.d]]:
					vec = [osx[0]]
					i = 0
					while i < 2:
						r = struct.pack("<B", random.randint(0, STATES - 1))
						if r not in vec:
							vec.append(r)
							i += 1
					random.shuffle(vec)
					vi = vec.index(osx[0])
					if my_vi == -1:
						my_vi = vi
					sends_rv[osx[1]] += vec[0]+vec[1]+vec[2]
					if osx[2] == None:
						self.vectorBQ.put(vi)
					else:
						sends_ri[osx[2]] += struct.pack("<B", vi)
				my_vis.append(my_vi)
			pvis.append(my_vis)
			for remote_server in [self.b, self.c, self.d, self.e, self.f]:
				remote_server.rvsock.sendall(sends_rv[remote_server])
				remote_server.risock.sendall(sends_ri[remote_server])
		presults = []
		debug_counter = 0
		for pi in range(len(pstates)):
			rstates = []
			debug_counter += 1
			for si in range(len(states)):
				index = struct.unpack("<BB", self.f.risock.recv(2))
				index = (index[1] << 8) + index[0]
				flip = struct.unpack("<B", self.f.risock.recv(1))[0]

				#small_lut = []
				#for i in range(4):
				#	row = self.b.rvsock.recv(128)
				#	if i == my_vis[si]:
				#		for by in row:
				#			small_lut.append(by)
				
				#rows = self.b.rvsock.recv(41*3)
				#small_lut = rows[41 * (2 - pvis[pi][si]): 41 * (2 - pvis[pi][si]) + 41] 
				#for by in row:
				#	small_lut.append(by)
	
				rows = self.b.rvsock.recv(243)
				small_lut = rows[81 * (pvis[pi][si]): 81 * (pvis[pi][si]) + 81] 
				rstates.append((struct.unpack("<B", small_lut[index])[0] ^ flip))
				#index2 = index >> 1
				#index22 = index % 2
				# TODO: Check for invalid state
				#rstates.append((struct.unpack("<B", small_lut[index])[0] ^ flip))
				#rstates.append(0)
			presults.append(rstates)
		return presults	


	def parreduce(self, states):
		rstates = []
		my_vis = []
		for state in states:
			osa = self.a.obfuscate(state)
			osb = self.b.obfuscate(state)
			osc = self.c.obfuscate(state)
			osd = self.d.obfuscate(state)
			ose = self.e.obfuscate(state)
			for remote_server in [self.b, self.c, self.d, self.e, self.f]:
				remote_server.q.put(struct.unpack("<B", remote_server.obfuscate(state))[0])
			my_vi = -1
			sends_rv = {}
			sends_ri = {}
			for remote_server in [self.b, self.c, self.d, self.e, self.f]:
				sends_rv[remote_server] = ""
				sends_ri[remote_server] = ""

			for osx in [[osa, self.b, self.f], [osb, self.c, None], [osc, self.d, self.b], [osd, self.e, self.c], [ose, self.f, self.d]]:
				vec = [osx[0]]
				i = 0
				while i < 2:
					r = struct.pack("<B", random.randint(0, STATES - 1))
					if r not in vec:
						vec.append(r)
						i += 1
				random.shuffle(vec)
				vi = vec.index(osx[0])
				if my_vi == -1:
					my_vi = vi
				sends_rv[osx[1]] += vec[0]+vec[1]+vec[2]
				if osx[2] == None:
					self.vectorBQ.put(vi)
				else:
					sends_ri[osx[2]] += struct.pack("<B", vi)
			my_vis.append(my_vi)
			for remote_server in [self.b, self.c, self.d, self.e, self.f]:
				remote_server.rvsock.sendall(sends_rv[remote_server])
				remote_server.risock.sendall(sends_ri[remote_server])

		for si in range(len(states)):
			index = struct.unpack("<BB", self.f.risock.recv(2))
			index = (index[1] << 8) + index[0]
			flip = struct.unpack("<B", self.f.risock.recv(1))[0]

			#small_lut = []
			#for i in range(4):
			#	row = self.b.rvsock.recv(128)
			#	if i == my_vis[si]:
			#		for by in row:
			#			small_lut.append(by)
			
			rows = self.b.rvsock.recv(128*4)
			row = rows[128 * (3 - my_vis[si]): 128 * (3 - my_vis[si]) + 128] 
			#for by in row:
			#	small_lut.append(by)


			# TODO: Check for invalid state
			#rstates.append((struct.unpack("<B", small_lut[index])[0] ^ flip))
			rstates.append(0)
		return rstates	

	def reduce(self, state):
		osa = self.a.obfuscate(state)
		osc = self.c.obfuscate(state)
		osd = self.d.obfuscate(state)
		ose = self.e.obfuscate(state)
		for remote_server in [self.b, self.c, self.d, self.e, self.f]:
			remote_server.q.put(struct.unpack("<B", remote_server.obfuscate(state))[0])

		my_vi = -1
		for osx in [[osa, self.b, self.f], [osc, self.d, self.b], [osd, self.e, self.c], [ose, self.f, self.d]]:
			vec = [osx[0]]
			i = 0
			while i < 3:
				r = struct.pack("<B", random.randint(0, STATES - 1))
				if r not in vec:
					vec.append(r)
					i += 1
			random.shuffle(vec)
			vi = vec.index(osx[0])
			if my_vi == -1:
				my_vi = vi
			osx[1].rvsock.sendall(vec[0]+vec[1]+vec[2]+vec[3])
			osx[2].risock.sendall(struct.pack("<B", vi))

		index = struct.unpack("<BB", self.f.risock.recv(2))
		index = (index[1] << 8) + index[0]
		flip = struct.unpack("<B", self.f.risock.recv(1))[0]

		small_lut = []
		for i in range(4):
			row = self.b.rvsock.recv(1024)
			if i == my_vi:
				for by in row:
					small_lut.append(by)
		
		# TODO: Check for invalid state
		return 0
		return (struct.unpack("<B", small_lut[index])[0] ^ flip)
		#print "Result fragment is %d" % (struct.unpack("<B", small_lut[index])[0] ^ flip)
		#sleep(1)

	def addVote(self):
		sleep(10)
		tally_window = []
		carry_window = []
		vote_window_len = self.tally_length / 3
		tand = 7
		for i in range(vote_window_len):
			tally_window.append((self.tally & tand) >> (i * 3))
			carry_window.append(None)
		while True:
			carry_window[0] = self.voteaddQ.get()
			states = []
			for i in range(vote_window_len):
				carry = carry_window[i]
				if carry == None:
					continue
				states.append(tally_window[i]  + (carry << 3))
			rstates = self.parreduces([states])[0]
			# rstates = self.parreduce(states)
			rsi = 0
			for i in range(vote_window_len):
				if carry_window[i] == None:
					continue
				carry_window[i] = rstates[rsi] & 1
				tally_window[i] = (rstates[rsi] >> 1)
				rsi += 1
			for i in range(vote_window_len-1, 0, -1):
				carry_window[i] = carry_window[i-1]
			print tally_window
