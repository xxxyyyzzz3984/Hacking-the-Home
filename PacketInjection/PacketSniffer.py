import socket
import binascii

'''Packet Sniffing for Linux'''

class PacketSniffer:
    def __init__(self, interface):
        self.soc = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 ** 30)
        self.interface = interface
        self.tcp_packet_hex = None

        '''Only for TCP case'''
        self.SrcMac_Start = 0
        self.SrcMac_End = 12

        self.DestMac_Start = 12
        self.DestMac_End = 24

        self.SrcIP_Start = 52
        self.SrcIP_End = 60

        self.DestIP_Start = 60
        self.DestIP_End = 68

        self.SrcPort_Start = 68
        self.SrcPort_End = 72

        self.DestPort_Start = 72
        self.DestPort_End = 76

        self.SeqNo_Start = 76
        self.SeqNo_End = 84

        self.AckSeqNo_Start = 84
        self.AckSeqNo_End = 92

        self.flags_Start = 92
        self.flags_End = 96

        self.payload_Start = 131

        try:
            self.soc.bind((self.interface, 0x0003))

        except socket.error:
            print 'Interface Not Found!'

    # use while true to get packets constantly
    def get_tcp_package(self):
        a = self.soc.recvfrom(65565)[0]
        h = binascii.hexlify(a)
        h = h.replace('\r', '').replace('\n', '').replace(' ','')

        # check if it is a tcp protocol
        if h[46:48] == '06':
            self.tcp_packet_hex = h
            return True

        else:
            return False