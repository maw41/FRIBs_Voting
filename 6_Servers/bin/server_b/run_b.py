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


a.id = 'A'
a.ip = '127.0.0.1'
a.seed = 'seed'
a.ports = [19800, 19801, 19810, 19811]
a.scheduler_port = 20000

c.id = 'C'
c.ip = '127.0.0.1'
c.seed = 'seed'
c.ports = [19822, 19823, 19812, 19813]

d.id = 'D'
d.ip = '127.0.0.1'
d.seed = 'seed'
d.ports = [19832, 19833, 19814, 19815]

e.id = 'E'
e.ip = '127.0.0.1'
e.seed = 'seed'
e.ports = [19842, 19843, 19816, 19817]

f.id = 'F'
f.ip = '127.0.0.1'
f.seed = 'seed'
f.ports = [19852, 19853, 19818, 19819]

a.olut = "%s/a.olut" % OLUT_DIR
b.olut = "%s/b.olut" % OLUT_DIR
c.olut = "%s/c.olut" % OLUT_DIR
d.olut = "%s/d.olut" % OLUT_DIR
e.olut = "%s/e.olut" % OLUT_DIR
f.olut = "%s/f.olut" % OLUT_DIR

config.ip = '0.0.0.0'
config.id = 1
config.scheduler_port = 20001
config.result_lut = "%s/result.lut" % OLUT_DIR
config.remote_servers = [b, c, d, e, f, a]
config.client_ip = '0.0.0.0'
config.client_port = 21001
config.init_tally = 0

controller = Controller(config)
controller.start()
while not controller.running.wait():
	pass
controller.stop()
