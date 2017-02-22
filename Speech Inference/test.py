from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.multiclass import OneVsOneClassifier, OutputCodeClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import tree

max_len = 300

packet_collect_dir = 'packet_collect/'
x_list = []
y_list = []

for i in range(1, 11):
    file_path = packet_collect_dir + 'speech%d.txt' % i
    f = open(file_path, 'r')
    for line in f:
        numbers_str = line.split(' ')[0: len(line.split(' ')) - 1]
        numbers = map(int, numbers_str)
        if len(numbers) < 20:
            continue

        for j in range(max_len - len(numbers)):
            numbers.append(0)

        x_list.append(numbers)
        y_list.append(i)

X = np.array(x_list)
Y = np.array(y_list)
clf = GaussianNB()
clf.fit(X, Y)


count = 0
for i in range(len(x_list)):
    if clf.predict(X[i].reshape(1,-1)) == y_list[i]:
        count += 1

print len(y_list)
print count
