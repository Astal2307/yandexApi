import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class FileStat(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(960, 540, 800, 500)
        self.info = QLabel('Введите координаты:', self)
        self.info.resize(400, 60)
        self.info.move(275, 30)

        self.image = QLabel(self)
        self.image.resize(self.geometry().width(), self.geometry().height())
        self.image.move(0, 0)

        self.line1 = QLineEdit(self)
        self.line1.resize(200, 50)
        self.line1.move(300, 100)
        self.line2 = QLineEdit(self)
        self.line2.resize(200, 50)
        self.line2.move(300, 200)

        self.btn = QPushButton('Отобразить карту', self)
        self.btn.resize(300, 100)
        self.btn.move(250, 400)
        self.btn.clicked.connect(self.show1)

        self.lbl = QLabel('Для переключения слоев карты нажимайте на кнопку Enter', self)
        self.lbl.resize(5000, 50)
        self.lbl.move(30, 300)

        self.zoom = 10
        self.l = 'map'
        self.ls = ['map', 'sat', 'sat,skl']
        self.map, self.sat, self.satskl = None, None, None
        self.ind = 0

    def keyPressEvent(self, e):
        k = e.key()
        if k == Qt.Key.Key_PageDown:
            if self.zoom <= 23:
                self.zoom += 1
        if k == Qt.Key.Key_PageUp:
            if self.zoom >= 1:
                self.zoom -= 1
        a, b = list(map(float, self.coords.split(',')))
        w, h = self.count_w(), self.count_h()
        if e.key() == Qt.Key.Key_Left:
            if a - w > -180:
                a -= w
        if e.key() == Qt.Key.Key_Right:
            if a + w < 180:
                a += w
        if e.key() == Qt.Key.Key_Down:
            if b - h > -90:
                b -= h
        if e.key() == Qt.Key.Key_Up:
            if b + h < 90:
                b += h

        if e.key() == Qt.Key.Key_Return:
            self.ind += 1

        self.coords = f'{a},{b}'
        self.lbl.move(30, 400)
        self.show1()

    def show1(self):
        import requests

        try:
            self.coords = f'{self.line1.text()},{self.line2.text()}'
        except Exception:
            pass

        map_request = f"http://static-maps.yandex.ru/1.x/"
        response_map = requests.get(map_request, params={'ll': self.coords,
                                                         'z': f'{self.zoom}',
                                                         'l': 'map'})

        response_sat = requests.get(map_request, params={'ll': self.coords,
                                                         'z': f'{self.zoom}',
                                                         'l': 'sat'})

        response_sat_skl = requests.get(map_request, params={'ll': self.coords,
                                                             'z': f'{self.zoom}',
                                                             'l': 'sat,skl'})

        print(response_map.url)

        """if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)"""

        with open('123.png', 'wb') as f:
            print(self.ind)
            if self.ind % 3 == 0:
                f.write(response_sat.content)
            if self.ind % 3 == 1:
                f.write(response_map.content)
            if self.ind % 3 == 2:
                f.write(response_sat_skl.content)
        self.pixmap = QPixmap()
        self.pixmap.load('123.png')
        self.image.setPixmap(self.pixmap)

        try:
            self.btn.deleteLater()
            self.line1.deleteLater()
            self.line2.deleteLater()
        except Exception:
            pass

    def count_h(self):
        return 180 / (2 ** (self.zoom + 8)) * 900

    def count_w(self):
        return 360 / (2 ** (self.zoom + 8)) * 800


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = FileStat()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
