import socket
import struct
import threading
import sys
import random
from threading import Thread


def intpack(i):
	return struct.pack('<BBBB', (i >> 24) & 255, (i >> 16) & 255, (i >> 8) & 255, i & 255)

if len(sys.argv) != 3:
	print 'This will add 1000 votes'
	print 'Usage: %s <start_voter_id> <num>' % sys.argv[0]
	exit()
start_voter_id = int(sys.argv[1])
number_of_votes = int(sys.argv[2])

print 'Please enter your vote for %s voters (y/n):' % number_of_votes,
v = sys.stdin.read(1)
print ''
vi = 0
if v == 'y':
	vi = 1

for voter_id in range(start_voter_id, start_voter_id+number_of_votes):
	print "Voter %d..." % voter_id,
	fragments = []
	ri = 0
	for i in range(2):
		fragments.append(random.randint(0,1))
		ri = ri ^ fragments[i]
	fragments.append(ri ^ vi)

	servers_config = [('127.0.0.1', 11000),('127.0.0.1', 11001),('127.0.0.1', 11002)]
	servers = []
	# Connect to all fragment servers first
	for server_config in servers_config:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((server_config[0], server_config[1]))
		servers.append(sock)
		
	# Send fragments
	for i in range(3):
		servers[i].sendall(intpack(voter_id) + struct.pack("<B", fragments[i]))

	# Get the acks
	for server in servers:
		server.close()
	print "Done."
