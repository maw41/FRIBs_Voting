import struct
import socket
import ssl
import sys
import thread
import random
import copy #TEMP
import time
from Queue import Queue
from time import sleep

class Server:
	def loadResultLut(path):
		return 0

class RemoteServer(Server):
	def __init__(self, ip=None, seed=None, rport=None, lport=None, sport=None):
		self.ip = ip
		self.rport = rport
		self.lport = lport if lport else rport
		self.scheduler_port = sport
		self.random = random.Random()
		self.random.seed(seed)

	def obfuscate(self, state):
		return self.olut[state]

	def send(self, b):
		self.ssl_sock.sendall(b)

	def connect(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		self.ssl_sock = ssl.wrap_socket(self.sock,cert_reqs=ssl.CERT_REQUIRED, ca_certs='server_cert.pem')
		try:
			self.ssl_sock.connect((self.ip, self.rport)) 
			print 'Connected'
			return True
		except:
			return False	

	def close(self):
		return self.ssl_sock.close()
	
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
	def __init__(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c
		self.qosb = Queue()
		self.qosc = Queue()
		self.voteaddQ = Queue()

	def initiateTally(self, value, length):
		assert(length % 3 == 0)	
		self.tally_length = length
		self.tally = value

	def listeningB(self):
		self.ssl_bsock.listen(10)
		conn, addr = self.ssl_bsock.accept() 
		print 'Listen Connected'
		while True:
			b1 = conn.recv(1)
			if len(b1) == 0:
				break
			ri = struct.unpack("<B", b1)[0]
			osb = self.qosb.get()
			osbf = 0
			for i in range(4):
				row_bytes = []
				for j in range(32):
					row_bytes.append(j)
				self.b.random.shuffle(row_bytes)
				osb_new = row_bytes.index(osb)
				for j in range(32):
					tmp_r = self.b.random.randint(0,31)
					if i == ri and j == osb_new:
						osbf = tmp_r
						osbi = osb_new

				
			conn.sendall(struct.pack("<B", osbi) + struct.pack("<B", osbf))
		self.ssl_bsock.close()
		thread.exit()

	def listeningC(self):
		self.ssl_csock.listen(10)
		conn, addr = self.ssl_csock.accept() 
		print 'Listen Connected'
		while True:
			b4 = conn.recv(4)
			if len(b4) == 0:
				break
			osc = self.qosc.get() * 32
			rbs = ''
			for i in range(4):
				i = (struct.unpack("<B",b4[i])[0] * 32 * 32) + osc
				row_bytes = self.result_lut[i:i+32] 
				self.c.random.shuffle(row_bytes)
				for rb in row_bytes:
					tmp_r = self.c.random.randint(0,31)
					rbs += struct.pack("<B", struct.unpack("<B", rb)[0] ^ tmp_r)
			conn.sendall(rbs)	
		self.ssl_csock.close()
		thread.exit()

	def listen(self):
		self.bsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bsock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		self.csock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		self.bsock.bind(('0.0.0.0', self.b.lport))
		self.csock.bind(('0.0.0.0', self.c.lport))
		self.ssl_bsock = ssl.wrap_socket(self.bsock, keyfile='server_key.pem', certfile='server_cert.pem', server_side=True)
		self.ssl_csock = ssl.wrap_socket(self.csock, keyfile='server_key.pem', certfile='server_cert.pem', server_side=True)
		thread.start_new_thread(self.listeningB, ())
		thread.start_new_thread(self.listeningC, ())
		thread.start_new_thread(self.addVote, ())

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
			vis = []
			sendb = ""
			sendc = ""
			for state in states:
				osa = self.a.obfuscate(state)
				self.qosb.put(struct.unpack("<B", self.b.obfuscate(state))[0])
				self.qosc.put(struct.unpack("<B", self.c.obfuscate(state))[0])
				vec = [osa]
				i = 0
				while i < 3:
					r = struct.pack("<B", random.randint(0, 31))
					if r not in vec:
						vec.append(r)
						i += 1
				random.shuffle(vec)
				vi = vec.index(osa)
				vis.append(vi)
				#self.b.sock.sendall(vec[0]+vec[1]+vec[2]+vec[3])
				#self.c.sock.sendall(struct.pack("<B", vi))
				sendb += vec[0]+vec[1]+vec[2]+vec[3]
				sendc += struct.pack("<B", vi)
			self.b.ssl_sock.sendall(sendb)
			self.c.ssl_sock.sendall(sendc)
			pvis.append(vis)

		presults = []
		for pi in range(len(pstates)):	
			results = []
			for si in range(len(pstates[pi])):
				small_lut = []
				rows = self.b.ssl_sock.recv(128)
				#row = rows[32 * (3 - pvis[pi][si]): 32 * (3 - pvis[pi][si]) + 32]
				row = rows[32 * vis[si]: 32 * vis[si] + 32]
				for by in row:
					small_lut.append(by)
				index = struct.unpack("<B", self.c.ssl_sock.recv(1))[0]
				flip = struct.unpack("<B", self.c.ssl_sock.recv(1))[0]
				results.append(struct.unpack("<B", small_lut[index])[0] ^ flip)
			presults.append(results)
		return presults


	def parreduce(self, states):
		vis = []
		sendb = ""
		sendc = ""
		for state in states:
			osa = self.a.obfuscate(state)
			self.qosb.put(struct.unpack("<B", self.b.obfuscate(state))[0])
			self.qosc.put(struct.unpack("<B", self.c.obfuscate(state))[0])
			vec = [osa]
			i = 0
			while i < 3:
				r = struct.pack("<B", random.randint(0, 31))
				if r not in vec:
					vec.append(r)
					i += 1
			random.shuffle(vec)
			vi = vec.index(osa)
			vis.append(vi)
			#self.b.sock.sendall(vec[0]+vec[1]+vec[2]+vec[3])
			#self.c.sock.sendall(struct.pack("<B", vi))
			sendb += vec[0]+vec[1]+vec[2]+vec[3]
			sendc += struct.pack("<B", vi)
		self.b.ssl_sock.sendall(sendb)
		self.c.ssl_sock.sendall(sendc)
	
		results = []
		for si in range(len(states)):
			small_lut = []
			rows = self.b.ssl_sock.recv(128)
			#row = rows[32 * (3 - vis[si]): 32 * (3 - vis[si]) + 32]
			row = rows[32 * vis[si]: 32 * vis[si] + 32]
			for by in row:
				small_lut.append(by)
			index = struct.unpack("<B", self.c.ssl_sock.recv(1))[0]
			flip = struct.unpack("<B", self.c.ssl_sock.recv(1))[0]
			results.append(struct.unpack("<B", small_lut[index])[0] ^ flip)
		return results

	def addVote(self):
		sleep(10)
		tally_window = []
		carry_window = []
		vote_window_len = self.tally_length / 4
		tand = 15
		for i in range(vote_window_len):
			tally_window.append((self.tally & tand) >> (i * 4))
			carry_window.append(None)
		while True:
			carry_window[0] = self.voteaddQ.get()
			states = []
			for i in range(vote_window_len):
				carry = carry_window[i]
				if carry == None:
					continue
				states.append((tally_window[i] << 1) + carry)
			#rstates = self.parreduces([states])[0] # Example for multiple tallies
			rstates = self.parreduce(states)
			rsi = 0
			for i in range(vote_window_len):
				if carry_window[i] == None:
					continue
				carry_window[i] = (rstates[rsi] & 16) >> 4
				tally_window[i] = (rstates[rsi] & 15)
				rsi += 1
			for i in range(vote_window_len-1, 0, -1):
				carry_window[i] = carry_window[i-1]
			print tally_window
			
			
		return
