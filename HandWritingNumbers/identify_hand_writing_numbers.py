
import input_data
import tensorflow as tf

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)


def weight_variable(shape, name=None):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial, name=name)


def bias_variable(shape, name=None):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial, name=name)


def conv2d(x, W, name=None):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME', name=name)


def max_pool_2x2(x, name=None):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name=name)


def naive_softmax():
    x = tf.placeholder('float', [None, 784])
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))
    y = tf.nn.softmax(tf.matmul(x, W) + b)
    y_ = tf.placeholder('float', [None, 10])
    # for training
    cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
    # for test
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

    init = tf.initialize_all_variables()
    with tf.Session() as sess:
        sess.run(init)
        writer = tf.summary.FileWriter('./graphs', sess.graph)
        for i in range(1000):
            batch_xs, batch_ys = mnist.train.next_batch(100)
            # print(batch_xs.shape, batch_ys.shape)
            _, loss = sess.run([train_step, cross_entropy], feed_dict={x: batch_xs, y_: batch_ys})
            print(loss)
        print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
        writer.close()


def cnn():
    sess = tf.InteractiveSession()
    x = tf.placeholder('float', [None, 784], name='x')
    y_ = tf.placeholder('float', [None, 10], name="y_")
    # reshape x to batch * h * w * channel
    x_image = tf.reshape(x, [-1, 28, 28, 1], name='x_img')
    # first convolve layer
    W_conv1 = weight_variable([5, 5, 1, 32], name='w_conv1')
    b_conv1 = bias_variable([32], name='b_conv1')
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1, name='h_conv1')
    # pooled
    h_pool1 = max_pool_2x2(h_conv1, name='h_pool1')
    # second convolve layer
    W_conv2 = weight_variable([5, 5, 32, 64], name='w_conv2')
    b_conv2 = bias_variable([64], name='b_conv2')
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2, name='h_conv2')
    # pooled
    h_pool2 = max_pool_2x2(h_conv2, name='h_pool2')

    W_fc1 = weight_variable([7 * 7 * 64, 1024], name='w_fc1')
    b_fc1 = bias_variable([1024], name='b_fc1')

    # full connected
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64], name='h_pool2_flat')

    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1, name='h_fc1')

    # drop out
    keep_prob = tf.placeholder("float", name='keep_prob')
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob, name='dropout')

    W_fc2 = weight_variable([1024, 10], name='w_fc2')
    b_fc2 = bias_variable([10], name='b_fc2')

    y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2, name='y_conv')

    # train & test
    cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv), name='x_entropy')
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"), name='accuracy')
    sess.run(tf.initialize_all_variables())
    writer = tf.summary.FileWriter('./graphs', sess.graph)
    # tootime-comsum
    for i in range(2000):
        batch = mnist.train.next_batch(50)
        if i % 100 == 0:
            train_accuracy = accuracy.eval(feed_dict={
                x: batch[0], y_: batch[1], keep_prob: 1.0})
            print("step %d, training accuracy %g" % (i, train_accuracy))
        train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

    # my compute cannot support the whole test set
    test = mnist.test.next_batch(1000)
    print("test accuracy %g" % accuracy.eval(feed_dict={
        x: test[0], y_: test[1], keep_prob: 1.0}))
    writer.close()


if __name__ == '__main__':
    import numpy as np
    cnn()
