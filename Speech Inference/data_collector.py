import time
import thread
from PacketSniffer import PacketSniffer
from PacketInjector import PacketInjector
import os

sound_dir = 'speech_train/'
speech_label = 1
packet_collect_dir = 'new_packet_collect/'
google_home_ip_hex = 'c0a80003'
thresh_len = 200 #threshold length of a packet, if <, drop
collect_duration = 20 #duration to collect packets
total_train_sound = 10 #total number of training sound files
each_train_trials = 200 #how many times each sound trains

def playsound(file_path):
    os.system('play ' + file_path)

packet_snf = PacketSniffer('wlan0')
packet_inj = PacketInjector('wlan0')

play_count = 0

while True:
    sound_filepath = sound_dir + str(speech_label) + '.wav'
    time.sleep(7)
    thread.start_new_thread(playsound, (sound_filepath, ))

    timeout = time.time() + collect_duration

    while True:
        tcp_flag = packet_snf.get_tcp_package()
        f = open(packet_collect_dir + 'speech%i.txt' % speech_label, 'a')

        if time.time() > timeout:
            print 'Collection timeout, break the loop!'
            f.write('\n')
            f.close()
            break

        if tcp_flag and \
            packet_snf.tcp_packet_hex[packet_snf.DestIP_Start:packet_snf.DestIP_End] == google_home_ip_hex:

            #useless traffic, skip
            if len(packet_snf.tcp_packet_hex) <= thresh_len:
                continue

            print 'collecting......'
            f.write(str(len(packet_snf.tcp_packet_hex)))
            f.write(' ')

    if play_count < each_train_trials:
        play_count += 1
    else:
        play_count = 0
        speech_label += 1

    if speech_label > total_train_sound:
        break
