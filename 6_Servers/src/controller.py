from server import LocalServer, RemoteServer
from scheduler import Scheduler
from client import Client
from time import sleep
from Queue import Queue
import threading
from threading import Thread
from time import sleep
import signal

class Controller:
	def __init__(self, config):
		self.client_queue = Queue()
		self.votes = {}
		self.scheduler = Scheduler(config.ip, config.scheduler_port, config.id)
		self.remote_servers = []
		for rs in config.remote_servers:
			if rs.ip == None:
				remote_server = RemoteServer()
			else:
				remote_server = RemoteServer(rs.ip, rs.seed, rs.ports[0], rs.ports[1], rs.ports[2], rs.ports[3], rs.id, rs.scheduler_port)
			remote_server.loadLut(rs.olut)
			self.remote_servers.append(remote_server)
		self.local_server = LocalServer(self.remote_servers)
		self.local_server.loadResultLut(config.result_lut)
		self.local_server.initiateTally(config.init_tally, 24)
		self.client_listener = Client(config.client_ip, config.client_port, self.client_queue)
		signal.signal(signal.SIGINT, self.stop)
		signal.signal(signal.SIGTERM, self.stop)


	def processVotePools(self):
		sleep(10)
		idle_count = 0
		while True:
			pool = self.scheduler.getNextPool()
			if pool == None or len(pool) == 0:
				sleep(0.5)
				#idle_count += 1
				#if idle_count > 20:
				#	for i in range((self.local_server.tally_length / 3) - 1):
				#		self.local_server.voteaddQ.put(None)
				#	idle_count = 0
				continue
			#idle_count = 0
			for v in pool:
				self.local_server.voteaddQ.put(self.votes[pool[v]])
			# TODO: remove this, it's only for examples
			for i in range(0,8):
				self.local_server.voteaddQ.put(0)
			#sleep(0.5)

	def handleNewVoter(self, in_queue):
		while True:
			voterID, vote = in_queue.get()
			if voterID not in self.votes:
				self.scheduler.newVoter(voterID)
				self.votes[voterID] = vote

	def start(self):
		self.scheduler.start()
		self.local_server.listen()
		for remote_server in self.remote_servers[1:]:
			while not remote_server.connect():
				sleep(0.25)
		for remote_server in self.remote_servers[1:]:
			if remote_server.scheduler_port == None:
				continue
			while not self.scheduler.connect(remote_server.ip, remote_server.scheduler_port):
				sleep(0.25)
		
		vpthread = Thread(target = self.processVotePools, args = ())
		vpthread.start()
		nvthread = Thread(target = self.handleNewVoter, args = (self.client_queue,))
		nvthread.start()
		self.client_listener.start()
		self.running = threading.Event()

	def stop(self):
		print "Stopping."
		self.client_listener.stop()

		for i in range(self.local_server.tally_length / 3):
			self.local_server.voteaddQ.put(None)
		sleep(5)
		self.scheduler.stop()
		for remote_server in self.remote_servers[1:]:
			remote_server.stop()
		print "Stopped"


