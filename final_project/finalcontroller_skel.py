# Final Skeleton
#
# Hints/Reminders from Lab 3:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:
#
# ip_header = packet.find('ipv4')
#
# if ip_header.srcip == "1.1.1.1":
#   print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. You must use ==.
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
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

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 3:
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # You should use these to determine where a packet came from. To figure out where a packet 
    # is going, you can use the IP header information.
    msg = of.ofp_flow_mod()
    m = of.ofp_flow_mod()

    # msg.idle_timeout = 50
    # msg.hard_timeout = 100


    ip = packet.find('ipv4')
    port = 0

    # SWITCHES 1, 2, 3, 5:
    # if the ip is not none, check which switch the packet is on, 
    # check for dst ip if it's meant for the host connected to the switch,
    # If so, fwd packet to appropriate port based on topology
    # Else, check for dst ip if packet is meant for host on another switch.
    # If so, send to port1 (switch4).
    # If dst ip is not one of these options, drop packet and return

    # FOR SWITCH 4
    # check for the srcip and dstip subnet range and fwd packets accordingly
    # to the correct switch_ID

    # if not an ip packet, floood
    if ip is not None: # packet is IP
      print("IP not none!", ip)
      msg.match = of.ofp_match.from_packet(packet)

      # SWITCH 1
      if switch_id == 1:
        if ip.dstip == "10.1.1.10":
          print("s1 receiving!")
          port = 8
          msg.actions.append(of.ofp_action_output(port=port))
          msg.data = packet_in
          self.connection.send(msg)
        else:
          print("s1 sending!")
          port = 1
          msg.actions.append(of.ofp_action_output(port=port))
          msg.data = packet_in
          self.connection.send(msg)

      # SWITCH 2
      elif switch_id == 2:
        if ip.dstip == "10.2.2.20":
          print("s2 received")
          port = 8
          msg.actions.append(of.ofp_action_output(port=port))
          msg.data = packet_in
          self.connection.send(msg)
        else:
          print("s2 sending!")
          port = 1
          msg.actions.append(of.ofp_action_output(port=port))
          msg.data = packet_in
          self.connection.send(msg)

      # SWITCH 3
      elif switch_id == 3:
        if ip.dstip == "10.3.3.30":
          print("s3 receiving!")
          port = 8
          msg.actions.append(of.ofp_action_output(port=port))
          msg.data = packet_in
          self.connection.send(msg)
        else:
          print("s3 sending!")
          port = 1
          msg.actions.append(of.ofp_action_output(port=port))
          msg.data = packet_in
          self.connection.send(msg)

      # SWITCH 4
      elif switch_id == 4:
        print("reached s4 :)")
        # h4 -> h5
        # if ip.srcip.inNetwork("123.45.67.89/24") and ip.dstip.inNetwork("10.5.5.50"):
        #   print("HACKER IP TO SERVER :( DRROOOPP")
        #   return

        # h# -> h1
        if ip.dstip.inNetwork("10.1.1.00/24"):
          print("going to switch 1!")
          port = 1
          msg.actions.append(of.ofp_action_output(port = port))
          msg.data = packet_in
          self.connection.send(msg)

        # h# -> h2
        if ip.dstip.inNetwork("10.2.2.00/24"):
          print("going to switch 2!")
          port = 2
          msg.actions.append(of.ofp_action_output(port = port))
          msg.data = packet_in
          self.connection.send(msg)

        # h# -> h3
        if ip.dstip.inNetwork("10.3.3.00/24"):
          print("going to switch 3!")
          port = 3
          msg.actions.append(of.ofp_action_output(port = port))
          msg.data = packet_in
          self.connection.send(msg)

        # h# -> h5, block from h4!
        if ip.dstip.inNetwork("10.5.5.00/24"):
          if ip.srcip.inNetwork("123.45.67.00/24"):
            print("HACKER IP TO SERVER H5 :( DDRROOOPP")
            return
          else:
            print("going to switch 5!")
            port = 4
            msg.actions.append(of.ofp_action_output(port = port))
            msg.data = packet_in
            self.connection.send(msg)

      # SWITCH 5
      elif switch_id == 5:
        if ip.dstip == "10.5.5.50":
          print("s5 receiving!")
          port = 8
          msg.actions.append(of.ofp_action_output(port=port))
          msg.data = packet_in
          self.connection.send(msg)
        else:
          print("s5 sending!")
          port = 1
          msg.actions.append(of.ofp_action_output(port=port))
          msg.data = packet_in
          self.connection.send(msg)

    else:
      # check if icmp packet from hacker h4
      icmp = packet.find('icmp') # search for icmp packet
      if icmp is not None:
        if icmp.srcip.inNetwork("123.45.67.00/24"):
          print("dropping ICMP from h4", icmp)
          return
          # print("flooood")
          # m.match = of.ofp_match.from_packet(packet)
          # m.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
          # m.data = packet_in
          # self.connection.send(m)
      else:
          print("flooood")
          m.match = of.ofp_match.from_packet(packet)
          m.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
          m.data = packet_in
          self.connection.send(m)











    # print "Example code."

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
