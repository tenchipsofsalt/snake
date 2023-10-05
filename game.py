# 3:44 - 4:18, 4:32 - 4:54
from collections import deque
from random import choice

class Snake:
    def __init__(self, start_x: int, start_y: int):
        self.head = [start_x, start_y, (0, 0)]
        self.joints = deque([])
        self.snakelen = 1

    # return if valid
    def move_snake(self, dir: tuple, should_increase: bool, avail: set) -> bool:
        # add head as joint if new dir different
        self.head[2] = dir
        if not self.joints or self.head[:2] != self.joints[-1][:2] and dir != self.joints[-1][2]:
            self.joints.append(self.head.copy())
        
        # move head
        self.head[0] += dir[0]
        self.head[1] += dir[1]
        avail.discard((self.head[0], self.head[1]))

        # move tail
        if not should_increase:
            avail.add((self.joints[0][0], self.joints[0][1]))
            self.joints[0][0] += self.joints[0][2][0]
            self.joints[0][1] += self.joints[0][2][1]
            if (len(self.joints) > 1 and self.joints[0][:2] == self.joints[1][:2]) or self.joints[0][:2] == self.head[:2]:
                self.joints.popleft()
        else:
            self.snakelen += 1

        # check head in body, linear time
        prev = self.head
        for joint in reversed(self.joints):
            zero_idx = joint[2].index(0)
            one_idx = 1 - zero_idx
            if self.head[zero_idx] == joint[zero_idx] and joint[2][one_idx] * joint[one_idx] <= joint[2][one_idx] * self.head[one_idx] < joint[2][one_idx] * prev[one_idx]:
                return False
            prev = joint
        return True

class SnakeGame:
    def __init__(self, m: int, n: int, starting_apps: int, start_x: int, start_y: int):
        # check edge cases
        if start_x < 0 or m < 0 or n < 0 or start_y < 0 or start_x >= m or start_y >= n:
            print("Invalid coordinates")
            return
        if starting_apps > m * n or starting_apps <= 0:
            print("Invalid number of apples")
            return
        
        self.r = m
        self.c = n
        
        # add available squares
        self.avail = set()
        for i in range(self.r):
            for j in range(self.c):
                self.avail.add((i, j))
        self.avail.remove((start_x, start_y))

        # dir dict
        self.inp_to_dir = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}

        # set of starting apples
        self.apps = set()
        while len(self.apps) < starting_apps:
            self.generate_apple()

        # init snake
        self.snake = Snake(start_x, start_y)

        # parse input until done
        self.parse_input()

        # print result
        self.print_score()

    def generate_apple(self):
        new_app = choice(tuple(self.avail))
        self.avail.remove(new_app)
        self.apps.add(new_app)

    def consume_apple(self, app):
        self.avail.add(app)
        self.apps.remove(app)
        self.generate_apple()

    def print_board(self):
        ret = []
        for i in range(self.r):
            line = []
            for j in range(self.c):
                if (i, j) in self.apps:
                    line.append('a')
                else:
                    line.append('.')
            ret.append(line)
        
        # print snake
        ret[self.snake.head[0]][self.snake.head[1]] = 'O'
        prev = self.snake.head
        for joint in reversed(self.snake.joints):
            cur = [prev[0] - joint[2][0], prev[1] - joint[2][1]]
            while True:
                ret[cur[0]][cur[1]] = 'O'
                if cur == joint[:2]:
                    break
                cur[0] -= joint[2][0]
                cur[1] -= joint[2][1]
            prev = joint
        print('\n'.join([''.join(line) for line in ret]))

    def try_move_dir(self, dir) -> bool:
        if not(0 <= dir[0] + self.snake.head[0] < self.r) or not (0 <= dir[1] + self.snake.head[1] < self.c) \
                or (self.snake.snakelen != 1 and self.snake.head[2] == (-dir[0], -dir[1])):
            print("Illegal move.\n")
        elif not(0 <= dir[0] + self.snake.head[0] < self.r) or not (0 <= dir[1] + self.snake.head[1] < self.c) \
                        or (self.snake.snakelen != 1 and self.snake.head[2] == (-dir[0], -dir[1])):
                print("Illegal move.\n")
        else:
            # check apple
            next_square = (self.snake.head[0] + dir[0], self.snake.head[1] + dir[1])
            if next_square in self.apps:
                self.consume_apple(next_square)
                self.snake.move_snake(dir, True, self.avail)
            elif not self.snake.move_snake(dir, False, self.avail):
                print("Game over, you moved into yourself.")
                return False
        return True

    def parse_input(self):
        while True:
            self.print_board()

            inp = input("Next move, or q to quit: ")

            # check for validity
            if inp == 'q':
                return
            elif inp not in self.inp_to_dir:
                print("Invalid input.\n")
            elif not self.try_move_dir(self.inp_to_dir[dir]):
                    return
        
    def print_score(self):
        print(f'Congratulations! You scored {self.snake.snakelen} points!')

SnakeGame(5, 5, 1, 2, 2)