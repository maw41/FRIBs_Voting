import socket
import struct
import threading
from threading import Thread

class Client:
	def __init__(self, server_ip, server_port, output_queue):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_address = (server_ip, server_port)
		self.out = output_queue
		pass
	
	def start(self):
		self.cthread = Thread(target = self.connecter, args = ())
		self.cthread.start()

	def stop(self):
		self.sock.setblocking(0)
		self.sock.close()

	def listener(self, connection):
		connection.setblocking(1)
		def unpackint(b):
			if len(b) != 4:
				return None
			sb = struct.unpack("<BBBB", b)
			return int(sb[3] + (sb[2] << 8) + (sb[1] << 16) + (sb[0] << 24))
		voter_id = unpackint(connection.recv(4))
		vote = struct.unpack('<B', connection.recv(1))[0] & 1
		self.out.put((voter_id, vote))
		connection.send('OK')
		connection.close()

	def connecter(self):
		self.sock.bind(self.server_address)
		self.sock.listen(1)
		while True:
			connection, client_address = self.sock.accept()
			if connection == None:
				Thread.exit()
			lthread = Thread(target = self.listener, args = (connection,))
			lthread.start()
