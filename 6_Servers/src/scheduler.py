import socket
import struct
import sys
import threading
from threading import Thread
from time import sleep #TEMP
from Queue import Queue
import hashlib

SERVERS = 6

class Scheduler:
	def __init__(self, server_ip, server_port, sid):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = (server_ip, server_port)
		self.client_socks = []
		self.sid = sid
		self.voterQ = Queue()
		self.rotateQ = Queue()
		self.rotateHashQ = Queue()
		self.rotateDoneQ = Queue()
		self.voterIDs = {}
		self.pools = []
		self.next_pool = 0
		self.pauseCondition = threading.Lock()
		self.sendingCondition = threading.Lock()
		self.nextCondition = threading.Condition()
		for i in range(SERVERS):
			self.pools.append({})
		self.nextnextPool = None
		self.nextPool = None

	def getNextPool(self):
		# Stop all transactions for a bit
		self.nextCondition.acquire()
		#self.pauseCondition.acquire()
		#print 'Started rotate'
		self.send('ROT', len(self.pools[self.sid]))
		server_rots = {} 
		server_rots[self.sid] = len(self.pools[self.sid])
		while len(server_rots) < SERVERS:
			sid, num = self.rotateQ.get()
			if sid not in server_rots:
				server_rots[sid] = num
			else:	
				self.rotateQ.put((sid,num))
		
		#print 'Got all rotate messages'
		while True:
			if len(self.pools[self.next_pool]) != server_rots[self.next_pool]:
				sleep(0.25)
			else:
				break
		#print 'Done rotate messages'
		server_rots_hash = {}
		h = hashlib.sha256(str(self.pools[self.next_pool])).digest()
		self.sendRotHash(h)
		server_rots_hash[self.sid] = h
		while len(server_rots_hash) < SERVERS:
			sid, h = self.rotateHashQ.get()
			if sid not in server_rots_hash:
				server_rots_hash[sid] = h




		for i in range(SERVERS - 1):
			if server_rots_hash[i] != server_rots_hash[i+1]:
				print 'Tampering!!!!!!'
				count0 = server_rots_hash.count(server_rots_hash[0])
				count1 = server_rots_hash.count(server_rots_hash[1])
				if count0 == SERVERS - 1 or count1 == SERVERS - 1:
					break
				else:
					prev_pool = (prev_pool - 1) % SERVERS
					if self.pools[prev_pool] == self.sid:
						for voter in self.pools[self.next_pool]: 
							index = len(self.pools[self.sid]) 
							self.pools[self.sid][index] = voter
							self.send('SET', voter, self.sid, index)
					self.next_pool = (self.next_pool + 1) % SERVERS
					return None

		#print 'Got all hashes'

		#np = self.nextPool
		#self.nextPool = self.nextnextPool
		#self.next_pool = (self.next_pool + 1) % SERVERS
		#self.nextnextPool = self.pools[self.next_pool]
		#self.pools[self.next_pool] = {}
		#self.pauseCondition.release()
		np = self.pools[self.next_pool]
		self.pools[self.next_pool] = {}
		self.next_pool = (self.next_pool + 1) % SERVERS
		#self.pauseCondition.rel	
		self.send('DRT', 0)
		server_rots = {} 
		server_rots[self.sid] = 1 
		while len(server_rots) < SERVERS:
			sid = self.rotateDoneQ.get()
			if sid not in server_rots:
				server_rots[sid] = 1
			else:	
				self.rotateDoneQ.put(sid)
		
		#print 'Got all rotate messages again'
		self.nextCondition.notify()
		self.nextCondition.release()
		return np

		
	def listener(self, connection):

		def unpackint(b):
			if len(b) != 4:
				return None
			sb = struct.unpack("<BBBB", b)
			return int(sb[3] + (sb[2] << 8) + (sb[1] << 16) + (sb[0] << 24))
		connection.send(str(self.sid))
		client_id = int(connection.recv(1))
		print 'scheduler: Server %s is connected' % client_id
		while True:
			cmd = connection.recv(3)
			if len(cmd) == 0:
				break
			if cmd == 'HAS':
				h = connection.recv(32)
				self.rotateHashQ.put((client_id, h))
				continue
			voter = unpackint(connection.recv(4))
			if cmd == 'DRT':
				self.rotateDoneQ.put(client_id)
			if cmd == 'ROT':
				self.rotateQ.put((client_id, voter))
			elif cmd == 'NEW':
				if voter not in self.voterIDs:
					self.voterIDs[voter] = []
				if client_id not in self.voterIDs[voter]:
					self.voterIDs[voter].append(client_id)
					if len(self.voterIDs[voter]) == SERVERS:
						ticket_server = voter % SERVERS
						if ticket_server == self.sid:
							self.voterQ.put(voter)
			elif cmd == 'SET':
				pool  = unpackint(connection.recv(4))
				index = unpackint(connection.recv(4))
				if index in self.pools[pool]:
					print 'oh dear :( conflict with pool %s and index %s' % (pool, index)
				self.pools[pool][index] = voter
	
	def stop(self):
		self.sock.close()				

	def processNewVoterQ(self):
		while True:
			voterID = int(self.voterQ.get())
			self.nextCondition.acquire()
			while self.next_pool == self.sid:
				self.nextCondition.wait() 
			pool = int(self.sid)
			index = len(self.pools[pool]) 
			self.pools[pool][index] = voterID
			self.send('SET', voterID, pool, index)
			self.nextCondition.release()

	def connecter(self):
		self.sock.bind(self.server_address)
		#self.sock.settimeout(10)
		self.sock.listen(1)
		while True:
			try:
				connection, client_address = self.sock.accept()
			except:
				break
			self.client_socks.append(connection)
			lthread = Thread(target = self.listener, args = (connection,))
			lthread.start()
		print 'Connecter closed'

	def sendRotHash(self, h):
		mess = 'HAS' + h
		self.sendingCondition.acquire()
		for connection in self.client_socks:
			connection.sendall(mess)
		self.sendingCondition.release()


	def send(self, cmd, voter, pool=None, index=None):
		def intpack(i):
			return struct.pack('<BBBB', (i >> 24) & 255, (i >> 16) & 255, (i >> 8) & 255, i & 255)
		mess = cmd + intpack(voter) 
		if pool != None:
			mess += intpack(pool)
			mess += intpack(index)
		self.sendingCondition.acquire()
		for connection in self.client_socks:
			connection.sendall(mess)
		self.sendingCondition.release()

	def newVoter(self, voter):
		#self.voterQ.put((self.sid, int(voterID)))
		if voter not in self.voterIDs:
			self.voterIDs[voter] = []
		if self.sid not in self.voterIDs[voter]:
			self.voterIDs[voter].append(self.sid)
			if len(self.voterIDs[voter]) == SERVERS:
				ticket_server = voter % SERVERS
				if ticket_server == self.sid:
					self.voterQ.put(voter)
		self.send('NEW', voter)

	def connect(self, client_ip, client_port):
		try:
			client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			client_sock.connect((client_ip, client_port))
			self.client_socks.append(client_sock)
			lthread = Thread(target = self.listener, args = (client_sock,))
			lthread.start()
			return True
		except:
			return False

	def start(self):
		cthread = Thread(target = self.connecter, args = ())
		qthread = Thread(target = self.processNewVoterQ, args = ())
		#tthread = Thread(target = self.processVoterTicketQ, args = ())
		cthread.start()
		qthread.start()
		#tthread.start()


