from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from constnts import BLOCK_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH


class Pacman:
    def __init__(self, window):
        self.last_x = 0,
        self.last_y = 25,
        self.x = 0
        self.y = 25
        self.is_moving = False
        self.stop = False
        self.move_src = 0
        self.move_dst = 0
        self.move_direction = 0
        self.lives = 3

        self.pixmap_right = QPixmap('static/pacman-right.png')
        self.pixmap_left = QPixmap('static/pacman-left.png')
        self.pixmap_up = QPixmap('static/pacman-up.png')
        self.pixmap_down = QPixmap('static/pacman-down.png')
        self.picture = QLabel(window)
        self.picture.setPixmap(self.pixmap_right)
        self.picture.move(self.x, self.y)
        self.picture.resize(25, 25)

    def move_iteration(self):
        if self.is_moving:
            self.last_x = self.x
            self.last_y = self.y
            if self.move_direction == 0:  # horizontal move
                if self.move_dst - self.move_src > 0:
                    if self.x + 2 < self.move_dst and self.x < WINDOW_WIDTH - BLOCK_SIZE:  # right
                        self.move_by(2, 0)
                    elif self.x < self.move_dst and self.x < WINDOW_WIDTH - BLOCK_SIZE:
                        self.move_by(1, 0)
                    else:
                        self.is_moving = False

                else:
                    if self.x - 2 > self.move_dst and self.x >= 0:  # left
                        self.move_by(-2, 0)
                    elif self.x > self.move_dst and self.x >= 0:
                        self.move_by(-1, 0)
                    else:
                        self.is_moving = False

            else:  # vertical move
                if self.move_dst - self.move_src > 0:
                    if self.y + 2 < self.move_dst and self.y < WINDOW_HEIGHT - BLOCK_SIZE * 2:  # down
                        self.move_by(0, 2)
                    elif self.y < self.move_dst and self.y < WINDOW_HEIGHT - BLOCK_SIZE * 2:
                        self.move_by(0, 1)
                    else:
                        self.is_moving = False
                else:
                    if self.y - 2 > self.move_dst and self.y >= 25:  # up
                        self.move_by(0, -2)
                    elif self.y > self.move_dst and self.y >= 25:
                        self.move_by(0, -1)
                    else:
                        self.is_moving = False

    def move_by(self, x, y):
        self.x += x
        self.y += y
        self.picture.move(self.x, self.y)

    def move_to(self, x, y):
        self.x = x
        self.y = y
        self.picture.move(self.x, self.y)

    def start_move(self, direction, step):
        if not self.is_moving:
            self.is_moving = True
            self.move_direction = direction
            if direction == 0:
                if step > 0:
                    self.picture.setPixmap(self.pixmap_right)
                else:
                    self.picture.setPixmap(self.pixmap_left)
                self.move_src = self.x
                self.move_dst = self.x + 1000 * step
            else:
                if step < 0:
                    self.picture.setPixmap(self.pixmap_up)
                else:
                    self.picture.setPixmap(self.pixmap_down)
                self.move_src = self.y
                self.move_dst = self.y + 1000 * step

    def end_move(self):
        if self.move_direction == 0:
            if self.move_dst > self.move_src:
                self.move_dst = self.x + BLOCK_SIZE - self.x % BLOCK_SIZE
            else:
                self.move_dst = self.x - self.x % BLOCK_SIZE
        else:
            if self.move_dst > self.move_src:
                self.move_dst = self.y + BLOCK_SIZE - self.y % BLOCK_SIZE
            else:
                self.move_dst = self.y - self.y % BLOCK_SIZE
