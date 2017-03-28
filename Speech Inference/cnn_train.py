import random
import numpy as np
import copy
import tensorflow as tf

########### reading data part ##############
train_speech_num = 10
max_len = 300
train_data_dir = './packet_collect/'
x_data_list = []
y_data_list = []
for i in range(1, train_speech_num+1):
    speech_file_path = train_data_dir + 'speech%d.txt' % i

    with open(speech_file_path, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            splited_line = line.split(' ')
            splited_line = splited_line[0: len(splited_line)-1]
            float_results = [float(j) for j in splited_line]

            if len(float_results) < 20:
                continue

            for j in range(max_len - len(float_results)):
                float_results.append(0.0)


            x_data_list.append(copy.copy(float_results))
            label = [0] * train_speech_num
            label[i-1] = 1
            y_data_list.append(copy.copy(label))
    f.close()

#### shuffle data
x_data = np.array(x_data_list)
y_data = np.array(y_data_list)
s = list(zip(x_data, y_data))
random.shuffle(s)
x_data, y_data = zip(*s)
x_data = np.array(x_data)
x_data = x_data.reshape([x_data.shape[0], x_data.shape[1], 1, 1])
y_data = np.array(y_data)
#####
##########

######### training part ##########
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 1, 1, 1], padding='SAME')

def max_pool_3x3(x):
    return tf.nn.max_pool(x, ksize=[1, 3, 3, 1], strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x1(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 1, 1], strides=[1, 1, 1, 1], padding='SAME')

def max_pool_3x1(x):
    return tf.nn.max_pool(x, ksize=[1, 3, 1, 1], strides=[1, 1, 1, 1], padding='SAME')

def conv2d_reduce(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 2, 2, 1], padding='SAME')

def max_pool_2x2_reduce(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

def max_pool_3x3_reduce(x):
    return tf.nn.max_pool(x, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')

def conv1d_reduce(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 2, 1, 1], padding='SAME')

def max_pool_2x1_reduce(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 1, 1], strides=[1, 2, 1, 1], padding='SAME')

def max_pool_3x1_reduce(x):
    return tf.nn.max_pool(x, ksize=[1, 3, 1, 1], strides=[1, 2, 1, 1], padding='SAME')

x = tf.placeholder("float", shape=[None, x_data.shape[1], 1, 1])
y_ = tf.placeholder("float", shape=[None, train_speech_num])

# convolutional layers
W_conv1 = weight_variable([7, 1, 1, 16])
b_conv1 = bias_variable([16])
h_conv1 = tf.nn.relu(conv2d(x, W_conv1) + b_conv1)
h_pool1 = max_pool_3x1_reduce(h_conv1)  ## one layer 3x3 max pooling
arr_size = max_len / 2

W_conv2 = weight_variable([5, 1, 16, 32])
b_conv2 = bias_variable([32])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_3x1_reduce(h_conv2)  ## one layer 2x2 max pooling
arr_size = arr_size / 2

W_conv3 = weight_variable([3, 1, 32, 32])
b_conv3 = bias_variable([32])
h_conv3 = tf.nn.relu(conv2d(h_pool2, W_conv3) + b_conv3)
h_pool3 = max_pool_2x1_reduce(h_conv3)  ## one layer 2x2 max pooling
arr_size = arr_size / 2

W_conv4 = weight_variable([2, 1, 32, 64])
b_conv4 = bias_variable([64])
h_conv4 = tf.nn.relu(conv2d(h_pool3, W_conv4) + b_conv4)


# fully connected layer
arr_size += 1
W_fc1 = weight_variable([arr_size * 64, 128])
b_fc1 = bias_variable([128])

h_pool2_flat = tf.reshape(h_conv4, [-1, arr_size * 64])  # flat into 1 dimention
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# dropout
keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob) # kill some neuron

# Readout Layer
W_fc2 = weight_variable([128, train_speech_num])
b_fc2 = bias_variable([train_speech_num])

y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

######################

###########training part
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))

mse = tf.reduce_mean(tf.square(y_-y_conv))


correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

train_step = tf.train.AdamOptimizer(1e-6).minimize(cross_entropy)

sess.run(tf.global_variables_initializer())
saver = tf.train.Saver()
# saver.restore(sess, './onet_train.ckpt')
# print 'Model restored.'
step = 0
total_err = 0
total_accuracy = 0

while True:

    if step >= x_data.shape[0]:
        print 'The average accuracy is %f.' % (total_accuracy/step)
        print 'The average error is %f.' % (total_err/step)
        print 'Saving model'

        save_path = saver.save(sess, save_path='./onet_train.ckpt')



        if (total_accuracy/step) > 0.99:
            print 'Stop training.'

        total_err = 0
        total_accuracy = 0
        step = 0

    x_data_batch = x_data[step]
    y_data_batch = y_data[step]

    x_data_batch = x_data_batch.reshape([1, max_len, 1, 1])
    y_data_batch = y_data_batch.reshape([1, train_speech_num])

    train_step.run({y_: y_data_batch, x: x_data_batch, keep_prob: 0.5}, sess)

    e = sess.run(mse, feed_dict={y_: y_data_batch, x: x_data_batch, keep_prob: 1.0})
    train_accuracy = accuracy.eval(feed_dict={y_: y_data_batch, x: x_data_batch, keep_prob: 1.0})

    total_err += e
    total_accuracy += train_accuracy

    step += 1


