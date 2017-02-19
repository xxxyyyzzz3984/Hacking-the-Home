import matplotlib.pyplot as plt

packet_collect_dir = 'packet_collect/'
max_len = 0
for i in range(10, 11):
    file_path = packet_collect_dir + 'speech%d.txt' %i
    f = open(file_path, 'r')
    for line in f:
        numbers_str = line.split(' ')[0: len(line.split(' '))-1]
        numbers = map(int, numbers_str)
        if len(numbers) > max_len:
            max_len = len(numbers)

print max_len