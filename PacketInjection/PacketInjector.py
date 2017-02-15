from socket import *
import binascii

from PacketSniffer import PacketSniffer

'''Sending raw packets'''

class PacketInjector:
    def __init__(self, interface):
        self.soc = socket(AF_PACKET, SOCK_RAW)
        self.soc.bind((interface, 0))

        self.SrcMac = None
        self.DestMac = None
        self.SrcIP= None
        self.DestIP = None
        self.SrcPort = None
        self.DestPort = None
        self.SeqNo = None
        self.AckSeqNo = None
        self.flags = None
        self.payload = None
        self.packet_hex = ""

        self.packetsnf = PacketSniffer(interface)

    def set_package(self, src_mac=None, dest_mac = None, src_ip=None, dest_ip=None,
                     src_port=None, dest_port=None, payload=None):
        self.SrcMac = src_mac
        self.DestMac = dest_mac
        self.SrcIP = src_ip
        self.DestIP = dest_ip
        self.SrcPort = src_port
        self.DestPort = dest_port
        self.payload = payload

    ## call this function after the sniffing begins!!!
    def inject_customized_packet(self):
        if self.SrcMac is not None:
            self.packet_hex += self.SrcMac
        else:
            self.packet_hex += \
                self.packetsnf.tcp_packet_hex[self.packetsnf.SrcMac_Start:self.packetsnf.SrcMac_End]

        if self.DestMac is not None:
            self.packet_hex += self.DestMac
        else:
            self.packet_hex += \
                self.packetsnf.tcp_packet_hex[self.packetsnf.DestMac_Start:self.packetsnf.DestMac_End]

        self.packet_hex += \
            self.packetsnf.tcp_packet_hex[self.packetsnf.DestMac_End:self.packetsnf.SrcIP_Start]

        if self.SrcIP is not None:
            self.packet_hex += self.SrcIP
        else:
            self.packet_hex += \
                self.packetsnf.tcp_packet_hex[self.packetsnf.SrcIP_Start:self.packetsnf.SrcIP_End]

        if self.DestIP is not None:
            self.packet_hex += self.DestIP
        else:
            self.packet_hex += \
                self.packetsnf.tcp_packet_hex[self.packetsnf.DestIP_Start:self.packetsnf.DestIP_End]

        if self.SrcPort is not None:
            self.packet_hex += self.SrcPort
        else:
            self.packet_hex += \
                self.packetsnf.tcp_packet_hex[self.packetsnf.SrcPort_Start:self.packetsnf.SrcPort_End]

        if self.DestPort is not None:
            self.packet_hex += self.DestPort
        else:
            self.packet_hex += \
                self.packetsnf.tcp_packet_hex[self.packetsnf.DestPort_Start:self.packetsnf.DestPort_End]

        ## seq no here
        self.packet_hex += self.packetsnf.tcp_packet_hex[self.packetsnf.DestPort_End:self.packetsnf.payload_Start]
        #########

        if self.payload is not None:
            self.packet_hex += self.payload
        else:
            self.packet_hex += \
                self.packetsnf.tcp_packet_hex[self.packetsnf.payload_Start:
                len(self.packetsnf.tcp_packet_hex)]


        raw = binascii.unhexlify(self.packet_hex)
        try:
            self.soc.send(raw)
        except error:
            pass
        self.packet_hex = ''
        self.packetsnf.tcp_packet_hex = ''


packinj = PacketInjector('wlp2s0')

while True:
    packinj.packetsnf.get_tcp_package()

    src_ip = packinj.packetsnf.tcp_packet_hex[packinj.packetsnf.DestIP_Start:packinj.packetsnf.DestIP_End]
    dest_ip = packinj.packetsnf.tcp_packet_hex[packinj.packetsnf.SrcIP_Start:packinj.packetsnf.SrcIP_Start]

    src_port = packinj.packetsnf.tcp_packet_hex[packinj.packetsnf.DestPort_Start:packinj.packetsnf.DestPort_End]
    dest_port = packinj.packetsnf.tcp_packet_hex[packinj.packetsnf.SrcPort_Start:packinj.packetsnf.SrcPort_End]


    if packinj.packetsnf.get_tcp_package():
        packinj.set_package(src_ip=src_ip, dest_ip=dest_ip, src_port=src_port, dest_port=dest_port)
        packinj.inject_customized_packet()
        print 'Packet Sent'