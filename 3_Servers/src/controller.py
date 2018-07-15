from server import LocalServer, RemoteServer
from scheduler import Scheduler
from client import Client
from time import sleep
from Queue import Queue
import threading
from threading import Thread
from time import sleep
import signal
import os

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
				remote_server = RemoteServer(rs.ip, rs.seed, rs.ports[0], rs.ports[1], rs.scheduler_port)
			remote_server.loadLut(rs.olut)
			self.remote_servers.append(remote_server)
		self.local_server = LocalServer(self.remote_servers[0], self.remote_servers[1], self.remote_servers[2])
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
				continue
				idle_count += 1
				if idle_count > 20:
					for i in range((self.local_server.tally_length / 4) - 1):
						self.local_server.voteaddQ.put(None)
					idle_count = 0
				continue
			idle_count = 0
			for v in pool:
				self.local_server.voteaddQ.put(self.votes[pool[v]])
			# TODO: remove this, it's only for examples
			#for i in range(0,6):
			#	self.local_server.voteaddQ.put(0)
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
		
		self.vpthread = Thread(target = self.processVotePools, args = ())
		self.vpthread.start()
		self.nvthread = Thread(target = self.handleNewVoter, args = (self.client_queue,))
		self.nvthread.start()
		self.client_listener.start()
		self.running = threading.Event()
		self.scheduler.setting_up.wait()
		print '\n\n\n\n'
		while True:
			cmd = raw_input("#> ")
			if cmd in ['stop', 'quit', 'exit', 'halt']:
				self.stop()
				break
			if cmd == 'print tally':
				num_votes, tally = self.local_server.getTally()
				print 'Number of votes: %s' % num_votes
				print 'Tally: %s' % tally
			elif cmd == 'flush tally':
				for i in range(0,6):
					self.local_server.voteaddQ.put(0)
			elif cmd == 'print stats':
				states_reached, states_trans = self.local_server.getStats()
				print 'States reached during processing:'
				for i in range(len(states_reached)):
					print 'State %s:\t%s' % (i, states_reached[i])
				print '\nStates transisitions from state 1:'
				for i in range(len(states_trans)):
					print 'State %s:\t%s' % (i, states_trans[i])

	def stop(self):
		print "Stopping."
		self.client_listener.stop()
		self.scheduler.stop()
		for remote_server in self.remote_servers[1:]:
			remote_server.stop()
		self.local_server.stop()
		self.running.clear()
		sleep(1)
		print "Stopped"
		os._exit(0)


