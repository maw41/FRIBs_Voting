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
a.ports = [19802, 19803, 19820, 19821]
a.scheduler_port = 20000

b.id = 'B'
b.ip = '127.0.0.1'
b.seed = 'seed'
b.ports = [19812, 19813, 19822, 19823]
b.scheduler_port = 20001

d.id = 'D'
d.ip = '127.0.0.1'
d.seed = 'seed'
d.ports = [19834, 19835, 19824, 19825]

e.id = 'E'
e.ip = '127.0.0.1'
e.seed = 'seed'
e.ports = [19844, 19845, 19826, 19827]

f.id = 'F'
f.ip = '127.0.0.1'
f.seed = 'seed'
f.ports = [19854, 19855, 19828, 19829]

a.olut = "%s/a.olut" % OLUT_DIR
b.olut = "%s/b.olut" % OLUT_DIR
c.olut = "%s/c.olut" % OLUT_DIR
d.olut = "%s/d.olut" % OLUT_DIR
e.olut = "%s/e.olut" % OLUT_DIR
f.olut = "%s/f.olut" % OLUT_DIR

config.ip = '0.0.0.0'
config.id = 2
config.scheduler_port = 20002
config.result_lut = "%s/result.lut" % OLUT_DIR
config.remote_servers = [c, d, e, f, a, b]
config.client_ip = '0.0.0.0'
config.client_port = 21002
config.init_tally = 0

controller = Controller(config)
controller.start()

while not controller.running.wait():
	pass

controller.stop()
print 'Done'
