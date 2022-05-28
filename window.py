from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from game import Game
from constnts import WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = None
        self.level_label = None
        self.level_score_label = None
        self.score_label = None
        self.lives_label = None
        self.button = None
        self.picture = None
        self.blocks = []
        self.game = None
        self.show_start_screen()

    def show_start_screen(self):
        self.__create_start_screen_background()
        self.__create_start_button()
        self.__set_window_properties()
        self.__create_menu_bar()
        self.show()

    def show_game_screen(self):
        if self.button is None:
            self.__remove_labels()
        if self.button is not None:
            self.__remove_start_screen()
        self.update()
        self.__show_characters()
        self.__create_score_label()
        self.show()

    def __start_game(self):
        self.__clean()
        if self.timer is not None:
            self.timer.stop()
        self.game = Game(self)
        self.show_game_screen()
        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(7)
        self.timer.timeout.connect(self.__game_iteration)
        self.timer.start()

    def __game_iteration(self):
        if self.game.level_changed:
            if self.game.actual_level_number > 3:
                self.close()
            self.game.levels[self.game.previous_level - 1].pacman.picture.hide()
            for ghost in self.game.levels[self.game.previous_level - 1].ghosts:
                ghost.picture.hide()
            self.game.level_changed = False
            self.__show_characters()
            self.update()
        self.game.game_iteration()

    def __create_menu_bar(self):
        menu_bar = self.menuBar()
        game_menu = QMenu("Gra", self)
        info_menu = QMenu("Informacje", self)
        menu_bar.addMenu(game_menu)
        start = QAction("Start", self)
        start.triggered.connect(self.__start_game)
        game_menu.addAction(start)
        quit = QAction("Wyjście", self)
        quit.triggered.connect(self.close)
        game_menu.addAction(quit)
        menu_bar.addMenu(info_menu)
        about_application = QAction("O aplikacji", self)
        about_application.triggered.connect(self.show_info_about_application)
        info_menu.addAction(about_application)

    def show_info_about_application(self):
        mbox = QMessageBox()
        mbox.setWindowTitle("O aplikacji")
        mbox.setText("Gra Pax-con - twórca Piotr Szymański")
        mbox.setStandardButtons(QMessageBox.Ok)
        mbox.exec_()

    def __create_start_button(self):
        self.button = QPushButton("START", self)
        self.button.setFont(QFont("Arial", 60))
        self.button.setStyleSheet("background-color: white")
        self.button.resize(400, 100)
        self.button.clicked.connect(lambda: self.__start_game())
        self.button.move(int(WINDOW_WIDTH / 3), int(WINDOW_HEIGHT / 2))

    def __create_start_screen_background(self):
        pixmap = QPixmap('static/pac-xon-deluxe.jpg')
        self.picture = QLabel(self)
        self.picture.setPixmap(pixmap)
        self.picture.move(0, 10)
        self.picture.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

    def __create_score_label(self):
        self.level_label = QLabel(self)
        self.level_label.setText("Poziom " + str(self.game.actual_level_number))
        self.level_label.setFont(QFont("Arial", 15))
        self.level_label.adjustSize()
        self.level_label.move(0, WINDOW_HEIGHT - 30)
        self.level_label.show()

        self.score_label = QLabel(self)
        self.score_label.setText("Punkty: " + str(self.game.score))
        self.score_label.setFont(QFont("Arial", 15))
        self.score_label.setFixedWidth(140)
        self.score_label.move(130, WINDOW_HEIGHT - 30)
        self.score_label.show()

        self.level_score_label = QLabel(self)
        self.level_score_label.setText("Wynik: 0/80%")
        self.level_score_label.setFont(QFont("Arial", 15))
        self.level_score_label.setFixedWidth(170)
        self.level_score_label.move(280, WINDOW_HEIGHT - 30)
        self.level_score_label.show()

        self.lives_label = QLabel(self)
        self.lives_label.setText("Zycia: " + str(self.game.actual_level.pacman.lives))
        self.lives_label.setFont(QFont("Arial", 15))
        self.lives_label.adjustSize()
        self.lives_label.move(450, WINDOW_HEIGHT - 30)
        self.lives_label.show()

    def __update_label(self, label, text):
        label.setText(text)

    def __set_window_properties(self):
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle("Pac-xon")

    def __remove_start_screen(self):
        self.button.setParent(None)
        self.button = None
        self.picture.setParent(None)
        self.picture = None

    def __show_characters(self):
        for ghost in self.game.actual_level.ghosts:
            ghost.picture.show()
        self.game.actual_level.pacman.picture.show()

    def __remove_labels(self):
        self.level_label.setParent(None)
        self.level_label = None
        self.lives_label.setParent(None)
        self.lives_label = None
        self.level_score_label.setParent(None)
        self.level_score_label = None
        self.score_label.setParent(None)
        self.score_label = None

    def __clean(self):
        if self.game is not None:
            self.game.actual_level.pacman.picture.setParent(None)
            self.game.actual_level.pacman.picture = None
            for ghost in self.game.actual_level.ghosts:
                ghost.picture.setParent(None)
                ghost.picture = None

    def paintEvent(self, event):
        if self.game is not None:
            self.game.actual_level.map.draw_map()
            self.__update_label(self.lives_label, "Zycia:" + str(self.game.actual_level.pacman.lives))
            self.__update_label(self.level_label, "Poziom:" + str(self.game.actual_level_number))
            self.__update_label(self.score_label, "Punkty:" + str(self.game.actual_level.map.filled_blocks_counter))
            self.__update_label(self.level_score_label, "Wynik:" +
                                str(int(self.game.actual_level.map.filled_blocks_counter
                                        / self.game.actual_level.map.blocks_number * 100)) + "/80%")
            if self.game.actual_level.game_over:
                self.__start_game()

    def keyPressEvent(self, event):
        if self.game is not None and not self.game.actual_level.game_over:
            if event.key() == Qt.Key_D:
                self.game.actual_level.pacman.start_move(0, 1)
            if event.key() == Qt.Key_A:
                self.game.actual_level.pacman.start_move(0, -1)
            if event.key() == Qt.Key_W:
                self.game.actual_level.pacman.start_move(1, -1)
            if event.key() == Qt.Key_S:
                self.game.actual_level.pacman.start_move(1, 1)

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        if self.game is not None:
            self.game.actual_level.pacman.end_move()
