import numpy as np


class MapSizeError(Exception):
    def __init__(self):
        super().__init__()


# snake game
# map settings:
# snake head~body   -   1~n
# food              -   -1
class Snake:
    def __init__(self, m_h=15, m_w=20):
        if m_h <= 0 or m_w <= 0 or m_h * m_w < 2:
            raise MapSizeError()
        self.__map = np.zeros([m_h, m_w], 'int32')
        self.__snake = []
        self.__birth()
        self.__update_food()
        self.game_over = False

    def reset(self):
        self.__map = np.zeros(self.__map.shape, 'int32')
        self.__snake = []
        self.__birth()
        self.__update_food()
        self.game_over = False
        return self.__map

    def __birth(self):
        if self.__snake:
            return
        snake_egg = np.hstack((np.random.randint(self.__map.shape[0], size=1), np.random.randint(self.__map.shape[1], size=1)))
        self.__snake.insert(0, snake_egg)
        self.__forward()
        directions = [
            np.array([0, 1]),
            np.array([1, 0]),
            np.array([0, -1]),
            np.array([-1, 0]),
        ]
        rd = np.random.randint(len(directions), size=1)[0]
        for r in range(rd, rd+4):
            head = snake_egg + directions[r%4]
            if not self.__is_out_of_bounds(head):
                self.__snake.insert(0, head)
                self.__forward()
                break

    def __update_food(self):
        max_idx = self.__map.shape[0] * self.__map.shape[1] - len(self.__snake)
        if max_idx == 0:
            # self.__game_over()
            return
        food_idx = np.random.randint(max_idx)
        for x in range(self.__map.shape[0]):
            for y in range(self.__map.shape[1]):
                if self.__map[x][y] == 0:
                    food_idx -= 1
                    if food_idx == 0:
                        self.__map[x][y] = -1
                        self.food = np.array((x, y), 'int32')

    def __game_over(self):
        self.game_over = True

    def __is_out_of_bounds(self, head):
        out_bounds = np.hstack((head < np.array([0, 0]), head >= np.array(self.__map.shape)))
        if np.any(out_bounds):
            return True

    def __is_self_bite(self, head):
        return len(self.__snake) > self.__map[head[0], head[1]] > 0

    def __is_dead(self, head):
        return self.__is_out_of_bounds(head) or self.__is_self_bite(head)

    def __try_eat(self):
        if self.__map[self.__snake[0][0], self.__snake[0][1]] == -1:
            self.__update_food()
            self.__map[self.__snake[0][0], self.__snake[0][1]] += 1
            return 1
        else:
            self.__map[self.__snake[-1][0], self.__snake[-1][1]] = 0
            self.__snake.pop()
            return 0

    def __forward(self):
        for body in self.__snake:
            self.__map[body[0], body[1]] += 1

    # take a step, return the observation after act, reward, finished or not, information
    def step(self, act):
        if self.game_over:
            return self.__map, 0, True, 'Game over!'
        dir_mat = {
            'GO_AHEAD': np.array([[1, 0], [0, 1]]),
            'TURN_LEFT': np.array([[0, 1], [-1, 0]]),
            'TURN_RIGHT': np.array([[0, -1], [1, 0]]),
        }
        direction = self.__snake[0] - self.__snake[1]
        direction = np.dot(direction.reshape((1, 2)), dir_mat[act])
        head = self.__snake[0] + direction.reshape(2)
        if self.__is_dead(head):
            self.__game_over()
            return self.__map, -1, True, 'Game over!'
        self.__snake.insert(0, head)
        r = self.__try_eat()
        self.__forward()
        return self.__map, r, False, ''

    def draw_map(self):
        if self.game_over:
            print('Game over!')
        for row in self.__map:
            for p in row:
                print(p, end=' ')
            print()

    def score(self):
        return len(self.__snake)

    def get_snake(self):
        return self.__snake


if __name__ == '__main__':
    snake = Snake(5, 10)
    snake.draw_map()
    while True:
        ipt = input()
        dir_list = ['GO_AHEAD','TURN_LEFT','TURN_RIGHT']
        try:
            cmd = dir_list[int(ipt)]
            print(snake.step(cmd))
            snake.draw_map()
        except IndexError:
            print('invalid cmd')
