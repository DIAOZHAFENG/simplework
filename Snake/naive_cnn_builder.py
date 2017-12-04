import tensorflow as tf


class NaiveCNNBuilder:
    def __init__(self, ipt, trainable=True):
        self.x = ipt
        self.trainable = trainable
        self.bottom = self.x

    @staticmethod
    def __weight_variable(shape, trainable=True, name=None):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial, trainable=trainable, name=name)

    @staticmethod
    def __bias_variable(shape, trainable=True, name=None):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial, trainable=trainable, name=name)

    @staticmethod
    def __conv2d(x, W, name=None):
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME', name=name)

    def add_conv_layer(self, out, activate=tf.nn.relu):
        shape = [int(i) for i in self.bottom.shape[1:]]
        shape.append(out)
        conv_w = NaiveCNNBuilder.__weight_variable(shape, self.trainable)
        conv_b = NaiveCNNBuilder.__bias_variable([out], self.trainable)
        conv_h = activate(NaiveCNNBuilder.__conv2d(self.bottom, conv_w) + conv_b)
        self.bottom = conv_h

    def add_pool_layer(self, pool_func=tf.nn.avg_pool, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1]):
        pool_h = pool_func(self.bottom, ksize=ksize, strides=strides, padding='SAME')
        self.bottom = pool_h

    def add_dense_layer(self, out, flat=False, activate=tf.nn.relu):
        if flat:
            self.bottom = tf.contrib.layers.flatten(self.bottom)
        shape = [int(i) for i in self.bottom.shape[1:]]
        shape.append(out)
        d_w = NaiveCNNBuilder.__weight_variable(shape, self.trainable)
        d_b = NaiveCNNBuilder.__bias_variable([out], self.trainable)
        d_h = activate(tf.matmul(self.bottom, d_w) + d_b)
        self.bottom = d_h
