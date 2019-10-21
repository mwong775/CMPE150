# Lab 3 Skeleton
#
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet.
    # print "Example Code." # part of starter code

    # "install" rule in switch
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    #
    msg.idle_timeout = 50
    msg.hard_timeout = 100

    p = packet.find('ipv4') # search for ipv4 packets

    if p is None: # not ipv4, check if ARP
      msg.data = packet_in
      arp = packet.find('arp') # search for arp packet
      if arp is None: # not arp, drop packet
        print "not ARP, dropping"
        msg.data = packet_in
        self.connection.send(msg)
      else: # arp, accept 
        print "accepting ARP"
        msg.data = packet_in
        msg.match.dl_type = 0x0806 # ethertype for arp
        a = of.ofp_action_output(port = of.OFPP_ALL)
        msg.actions.append(a)
        self.connection.send(msg)
    else: # ipv4 packet
      tcp = packet.find('tcp') # search for tcp packet
      if tcp is None: # not tcp, drop packet
        print "not TCP, dropping"
        msg.data = packet_in
        self.connection.send(msg)
      else: # tcp, accept
        print "accepting TCP"
        msg.data = packet_in
        msg.nw_proto = 6 # tcp protocol number
        a = of.ofp_action_output(port = of.OFPP_ALL)
        msg.actions.append(a)
        self.connection.send(msg)

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
