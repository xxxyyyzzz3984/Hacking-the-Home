from socket import *
import binascii


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


    def set_package(self, src_mac=None, dest_mac = None, src_ip=None, dest_ip=None,
                     src_port=None, dest_port=None, payload=None):
        self.SrcMac = src_mac
        self.DestMac = dest_mac
        self.SrcIP = src_ip
        self.DestIP = dest_ip
        self.SrcPort = src_port
        self.DestPort = dest_port
        self.payload = payload


    def send_raw_hex(self, hex):
        raw = binascii.unhexlify(hex.strip())
        try:
            self.soc.send(raw)
        except error:
            pass
