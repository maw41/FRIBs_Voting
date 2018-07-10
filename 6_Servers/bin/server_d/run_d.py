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
a.ports = [19804, 19805, 19830, 19831]
a.scheduler_port = 20000

b.id = 'B'
b.ip = '127.0.0.1'
b.seed = 'seed'
b.ports = [19814, 19815, 19832, 19833]
b.scheduler_port = 20001

c.id = 'C'
c.ip = '127.0.0.1'
c.seed = 'seed'
c.ports = [19824, 19825, 19834, 19835]
c.scheduler_port = 20002

e.id = 'E'
e.ip = '127.0.0.1'
e.seed = 'seed'
e.ports = [19846, 19847, 19836, 19837]

f.id = 'F'
f.ip = '127.0.0.1'
f.seed = 'seed'
f.ports = [19856, 19857, 19838, 19839]

a.olut = "%s/a.olut" % OLUT_DIR
b.olut = "%s/b.olut" % OLUT_DIR
c.olut = "%s/c.olut" % OLUT_DIR
d.olut = "%s/d.olut" % OLUT_DIR
e.olut = "%s/e.olut" % OLUT_DIR
f.olut = "%s/f.olut" % OLUT_DIR

config.ip = '0.0.0.0'
config.id = 3
config.scheduler_port = 20003
config.result_lut = "%s/result.lut" % OLUT_DIR
config.remote_servers = [d, e, f, a, b, c]
config.client_ip = '0.0.0.0'
config.client_port = 21003
config.init_tally = 0

controller = Controller(config)
controller.start()

while not controller.running.wait():
	pass

controller.stop()
print 'Done'
