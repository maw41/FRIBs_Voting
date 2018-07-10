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
a.ports = [19806, 19807, 19840, 19841]
a.scheduler_port = 20000

b.id = 'B'
b.ip = '127.0.0.1'
b.seed = 'seed'
b.ports = [19816, 19817, 19842, 19843]
b.scheduler_port = 20001

c.id = 'C'
c.ip = '127.0.0.1'
c.seed = 'seed'
c.ports = [19826, 19827, 19844, 19845]
c.scheduler_port = 20002

d.id = 'D'
d.ip = '127.0.0.1'
d.seed = 'seed'
d.ports = [19836, 19837, 19846, 19847]
d.scheduler_port = 20003

f.id = 'F'
f.ip = '127.0.0.1'
f.seed = 'seed'
f.ports = [19858, 19859, 19848, 19849]

a.olut = "%s/a.olut" % OLUT_DIR
b.olut = "%s/b.olut" % OLUT_DIR
c.olut = "%s/c.olut" % OLUT_DIR
d.olut = "%s/d.olut" % OLUT_DIR
e.olut = "%s/e.olut" % OLUT_DIR
f.olut = "%s/f.olut" % OLUT_DIR

config.ip = '0.0.0.0'
config.id = 4
config.scheduler_port = 20004
config.result_lut = "%s/result.lut" % OLUT_DIR
config.remote_servers = [e, f, a, b, c, d]
config.client_ip = '0.0.0.0'
config.client_port = 21004
config.init_tally = 0

controller = Controller(config)
controller.start()

while not controller.running.wait():
	pass

controller.stop()
print 'Done'
