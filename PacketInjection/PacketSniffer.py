import socket
import binascii

'''Packet Sniffing for Linux'''

class PacketSniffer:
    def __init__(self, interface):
        self.soc = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 ** 30)
        self.interface = interface

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
            self.SrcMac = h[0:12]
            self.DestMac = h[12:24]
            self.totallen = h[32:36]

            self.SrcIP = h[52:60]
            self.DestIP = h[60:68]

            self.SrcPort = h[68:72]
            self.DestPort = h[72:76]

            self.SeqNo = h[76:84]
            self.AckSeqNo = h[84:92]



packetsniffer = PacketSniffer('wlp2s0')
while True:
    packetsniffer.get_tcp_package()