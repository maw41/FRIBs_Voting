import socket
import struct
import threading
import sys
import random
from threading import Thread
import time 

g = [[1,0,0,1,1,0], [0,1,0,1,0,1], [0,0,1,0,1,1]]

def intpack(i):
	return struct.pack('<BBBB', (i >> 24) & 255, (i >> 16) & 255, (i >> 8) & 255, i & 255)


print 'Please enter your vote 100 voters (y/n):',
v = sys.stdin.read(1)
print ''
vi = 0
if v == 'y':
	vi = 1
for voter_id in range(10000, 10100):

	fragments = []
	ri = 0
	for i in range(2):
		fragments.append(random.randint(0,1))
		ri = ri ^ fragments[i]
	fragments.append(ri ^ vi)
	fragments6 = []
	for j in range(6):
		o = (((int(fragments[0]) * g[0][j]) + (int(fragments[1]) * g[1][j]) + (int(fragments[2]) * g[2][j])) % 2)
		fragments6.append(o)

	print fragments6
	servers_config = [('127.0.0.1', 21000),('127.0.0.1', 21001),('127.0.0.1', 21002),('127.0.0.1', 21003),('127.0.0.1', 21004),('127.0.0.1', 21005)]
	servers = []
	# Connect to all fragment servers first
	for server_config in servers_config:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((server_config[0], server_config[1]))
		servers.append(sock)
		
	# Send fragments
	for i in range(6):
		servers[i].sendall(intpack(voter_id) + struct.pack("<B", fragments6[i]))

	# Get the acks
	for server in servers:
		server.recv(3)
		server.close()
	time.sleep(0.05)
