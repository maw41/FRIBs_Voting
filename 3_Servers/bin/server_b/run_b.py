from controller import Controller
from config import Config, RemoteServerConfig


#a = RemoteServer()
#b = RemoteServer('127.0.0.1', "seed1", 19872, 19870)
#c = RemoteServer('127.0.0.1', "seed2", 19873, 19871)

OLUT_DIR = "tables/"
config = Config()
a = RemoteServerConfig()
b = RemoteServerConfig()
c = RemoteServerConfig()

a.id = 'A'
a.ip = '127.0.0.1'
a.seed = 'seed'
a.ports = [19870, 19872]
a.scheduler_port = 20000

#b.id = 'B'
#b.ip = '127.0.0.1'
#b.seed = 'seed'
#b.ports = [19872, 19870]
#b.scheduler_port = 20001

c.id = 'C'
c.ip = '127.0.0.1'
c.seed = 'seed'
c.ports = [19875, 19876]


a.olut = "%s/a.olut" % OLUT_DIR
b.olut = "%s/b.olut" % OLUT_DIR
c.olut = "%s/c.olut" % OLUT_DIR

config.ip = '127.0.0.1'
config.id = 1
config.scheduler_port = 20001
config.result_lut = "%s/result.lut" % OLUT_DIR
config.remote_servers = [b, c, a]
config.client_ip = '127.0.0.1'
config.client_port = 11001
config.init_tally = 0

controller = Controller(config)
controller.start()

while not controller.running.wait():
	pass

controller.stop()
print 'Done'
