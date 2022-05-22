import random
from ghost_type import GhostType
from constnts import WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class Ghost:
    def __init__(self, ghost_type, window):
        self.x = random.randint(BLOCK_SIZE, WINDOW_WIDTH - 2 * BLOCK_SIZE)
        self.y = random.randint(BLOCK_SIZE * 2, WINDOW_HEIGHT - 3 * BLOCK_SIZE)
        self.type = ghost_type
        if random.randint(0, 1) == 1:
            self.x_velocity = 2
        else:
            self.x_velocity = -2
        if random.randint(0, 1) == 1:
            self.y_velocity = 2
        else:
            self.y_velocity = -2

        if ghost_type == GhostType.PURPLE:
            picture_path = 'static/purple-ghost.png'
        elif ghost_type == GhostType.RED:
            picture_path = 'static/red-ghost.png'
        else:
            picture_path = 'static/orange-ghost.png'

        pixmap = QPixmap(picture_path)
        self.picture = QLabel(window)
        self.picture.setPixmap(pixmap)
        self.picture.move(self.x, self.y)
        self.picture.resize(25, 25)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.picture.move(self.x, self.y)
