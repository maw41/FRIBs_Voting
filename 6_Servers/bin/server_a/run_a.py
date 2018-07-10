from controller import Controller
from config import Config, RemoteServerConfig
from time import sleep

OLUT_DIR = "tables/"

config = Config()
a = RemoteServerConfig()
b = RemoteServerConfig()
c = RemoteServerConfig()
d = RemoteServerConfig()
e = RemoteServerConfig()
f = RemoteServerConfig()

b.id = 'B'
b.ip = '127.0.0.1'
b.seed = 'seed'
b.ports = [19810, 19811, 19800, 19801]

c.id = 'C'
c.ip = '127.0.0.1'
c.seed = 'seed'
c.ports = [19820, 19821, 19802, 19803]

d.id = 'D'
d.ip = '127.0.0.1'
d.seed = 'seed'
d.ports = [19830, 19831, 19804, 19805]

e.id = 'E'
e.ip = '127.0.0.1'
e.seed = 'seed'
e.ports = [19840, 19841, 19806, 19807]

f.id = 'F'
f.ip = '127.0.0.1'
f.seed = 'seed'
f.ports = [19850, 19851, 19808, 19809]

a.olut = "%s/a.olut" % OLUT_DIR
b.olut = "%s/b.olut" % OLUT_DIR
c.olut = "%s/c.olut" % OLUT_DIR
d.olut = "%s/d.olut" % OLUT_DIR
e.olut = "%s/e.olut" % OLUT_DIR
f.olut = "%s/f.olut" % OLUT_DIR

config.ip = '0.0.0.0'
config.id = 0
config.scheduler_port = 20000
config.result_lut = "%s/result.lut" % OLUT_DIR
config.remote_servers = [a, b, c, d, e, f]
config.client_ip = '0.0.0.0'
config.client_port = 21000
config.init_tally = 0

controller = Controller(config)
controller.start()
while not controller.running.wait():
	pass
controller.stop()
