from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class SwitchController:
  def __init__(self, dpid, connection):
    self.dpid = dpid
    self.connection = connection
    self.connection.addListeners(self)
    self.hostToPort = {}

  def _handle_PacketIn(self, event):
    packet = event.parsed
    log.info("Packet arrived to switch %s from %s to %s", self.dpid, packet.src, packet.dst)
    if packet.src not in self.hostToPort:
      self.hostToPort[packet.src] = event.port
      self.addNewTableEntryFromPacket(packet, event.port)

    if packet.dst not in self.hostToPort:
      log.info("Switch %s do not know the route to %s. Flooding", self.dpid, packet.dst)
      self.flood(event)
    elif self.hostToPort[packet.dst] == event.port:
      log.info("Packet was already recieved by host. Dropping")
      self.drop()
    else:
      log.info("Switch %s knows the route to %s. Forwarding", self.dpid, packet.dst)
      self.forward(event, self.hostToPort[packet.dst])

  def addNewTableEntryFromPacket(self, packet, portIn):
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet, portIn).flip()
    msg.actions.append(of.ofp_action_output(port = portIn))
    self.connection.send(msg)
    log.info("Adding new entry in flow table for switch %s, from %s to %s", self.dpid, packet.src, packet.dst)

  def flood(self, event):
    pass
    # packet = event.parsed
    # msg = of.ofp_packet_out()
    # msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    # msg.data = event.ofp
    # msg.in_port = event.port
    # self.connection.send(msg)

  def drop (self, event):
    pass

  def forward(self, event, port):
    pass
    # packet = event.parsed
    # msg = of.ofp_packet_out()
    # msg.actions.append(of.ofp_action_output(port = port))
    # msg.data = event.ofp
    # msg.in_port = event.port
    # self.connection.send(msg)
