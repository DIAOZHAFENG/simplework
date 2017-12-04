import tensorflow as tf
import numpy as np

from naive_cnn_builder import NaiveCNNBuilder as builder
from Snake import Snake

MAP_SIZE = [3, 4]
RECORD_SIZE = 500
BATCH_SIZE = 50
MAX_EPISODE = 2000
CHECK_POINT = 200
REPLACE_ITR = 200
GAMMA = 0.9
LR = 0.001
ACT_NUM = 3
EPSILON = 0.1
act_list = ['GO_AHEAD', 'TURN_LEFT', 'TURN_RIGHT']


class NaiveDQNPlayer():
    def __init__(self, map_size=MAP_SIZE, record_size=RECORD_SIZE, batch=BATCH_SIZE,
                 replace_itr=REPLACE_ITR, gamma=GAMMA, learning_rate=LR, acts=ACT_NUM, epsilon=EPSILON):
        self.map_size = map_size
        self.record = np.zeros((record_size, np.multiply.reduce(map_size) * 2 + 2))
        self.record_size = record_size
        self.batch = batch
        self.step = 0
        self.replace_itr = replace_itr
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.acts = acts
        self.epsilon = epsilon

        self.sess = tf.Session()
        self.s = tf.placeholder(tf.float32, [None] + map_size + [1], 's')
        self.s_ = tf.placeholder(tf.float32, [None] + map_size + [1], 's_')
        self.r = tf.placeholder(tf.float32, [None, ], name='r')  # input Reward
        self.a = tf.placeholder(tf.int32, [None, ], name='a')  # input Action
        with tf.variable_scope('eval_dqn'):
            self.eval_dqn = self.build_network(self.s)
        with tf.variable_scope('target_dqn'):
            self.target_dqn = self.build_network(self.s_)

        self.take_step = tf.arg_max(self.eval_dqn, 1, name='choose_action')

        # networks parameters
        eval_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='eval_dqn')
        target_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='target_dqn')

        with tf.variable_scope('q_target'):
            q_target = self.r + self.gamma * tf.reduce_max(self.target_dqn, axis=1, name='Qmax_s_')  # shape=(None, )
            self.q_target = tf.stop_gradient(q_target)
        with tf.variable_scope('q_eval'):
            a_indices = tf.stack([tf.range(tf.shape(self.a)[0], dtype=tf.int32), self.a], axis=1)
            self.q_eval_wrt_a = tf.gather_nd(params=self.eval_dqn, indices=a_indices)  # shape=(None, )
        with tf.variable_scope('loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval_wrt_a, name='TD_error'))
        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.learning_rate).minimize(self.loss)

        # target net replacement
        self.soft_replace = [tf.assign(t, e) for t, e in zip(target_params, eval_params)]

        # $ tensorboard --logdir=logs
        tf.summary.FileWriter("logs/", self.sess.graph)

        self.sess.run(tf.global_variables_initializer())

        self.cost_history = []

        self.ckpt_count = 0

    def add_record(self, s, a, r, s_):
        self.record[self.step % self.record_size] = np.hstack((s.flat, a, r, s_.flat))
        self.step += 1

    def build_network(self, ipt):
        nw = builder(ipt)
        # conv 1
        nw.add_conv_layer(32)
        # pool 1
        # nw.add_pool_layer()
        # conv 2
        nw.add_conv_layer(64)
        # pool 2
        # nw.add_pool_layer()
        # densely connected layer
        nw.add_dense_layer(1024, True)
        # output 0~goahead 1~turn_left 2~turn_right
        nw.add_dense_layer(self.acts)
        return nw.bottom

    def choose_action(self, s, training=True):
        a = self.sess.run(self.take_step, {self.s: s.reshape(np.hstack(([1], s.shape, [1])))})
        return a

    def learn(self):
        if self.batch > min(self.step, self.record_size):
            return
        sample_index = np.random.choice(min(self.step, self.record_size), size=self.batch)
        sample = self.record[sample_index]
        map_len = np.multiply.reduce(self.map_size)
        map_shape = [-1]
        map_shape.extend(self.map_size)
        map_shape.append(1)
        _, cost = self.sess.run([self._train_op, self.loss],
                                feed_dict={
                                    self.s: sample[:, :map_len].reshape(map_shape),
                                    self.a: sample[:, map_len].astype(int),
                                    self.r: sample[:, map_len + 1],
                                    self.s_: sample[:, -map_len:].reshape(map_shape),
                                })
        # soft target replacement
        if self.step % self.replace_itr == 0:
            self.sess.run(self.soft_replace)

        self.cost_history.append(cost)

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_history)), self.cost_history)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()

    def save(self):
        from time import time
        saver = tf.train.Saver()
        saver.save(self.sess, "/models/model_{}_{}.ckpt".format(self.ckpt_count, time()))
        print('save', self.ckpt_count)
        self.ckpt_count += 1


def naive_action_plan(snake, food):
    food_dir = food - snake[0]
    head_dir = snake[0] - snake[1]

    if head_dir[1] == 0:
        if head_dir[0] == -1:
            food_dir *= -1
    elif head_dir[1] == 1:
        food_dir = np.array((food_dir[1], -food_dir[0]))
    elif head_dir[1] == -1:
        food_dir = np.array((-food_dir[1], food_dir[0]))

    if food_dir[0] > 0:
        return 0
    elif food_dir[1] > 0:
        return 1
    elif food_dir[1] < 0:
        return 2
    else:
        return int(np.random.randint(1, 3, []))

if __name__ == '__main__':
    env = Snake(MAP_SIZE[0], MAP_SIZE[1])
    player = NaiveDQNPlayer(MAP_SIZE)
    for i in range(MAX_EPISODE):
        s = env.reset()
        step = 0
        policy = np.random.rand(1)[0] < EPSILON + i * 0.0005
        while not env.game_over:
            a = 0
            if policy or step > 100:
                a = int(player.choose_action(s))
            else:
                a = naive_action_plan(env.get_snake(), env.food)
            s_, r, _, _ = env.step(act_list[a])
            player.add_record(s, a, r, s_)
            s = s_
            if player.step >= player.batch and player.step % 5 == 0:
                player.learn()
            step += 1
        print(i, ':', env.score(), ',', step)
        if (i + 1) % CHECK_POINT == 0:
            player.save()
    player.plot_cost()
