from pox.core import core
import pox.openflow.discovery
from pox.lib.util import dpid_to_str
from extensions.switch import SwitchController

log = core.getLogger()

class Controller:
  def __init__ (self):
    self.connections = set()
    self.switches = []

    core.call_when_ready(self.startup, ('openflow', 'openflow_discovery'))

  def startup(self):
    core.openflow.addListeners(self)
    core.openflow_discovery.addListeners(self)
    log.info('Controller initialized')

  def _handle_ConnectionUp(self, event):
    log.info("Switch %s has come up.", dpid_to_str(event.dpid))
    if (event.connection not in self.connections):
      self.connections.add(event.connection)
      sw = SwitchController(event.dpid, event.connection)
      self.switches.append(sw)

  def _handle_LinkEvent(self, event):
    link = event.link
    log.info("Link has been discovered from %s,%s to %s,%s", dpid_to_str(link.dpid1), link.port1, dpid_to_str(link.dpid2), link.port2)

def launch():
  pox.openflow.discovery.launch()
  core.registerNew(Controller)
