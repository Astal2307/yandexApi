import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap


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
        self.btn.move(100, 400)
        self.btn.clicked.connect(self.show1)

    def show1(self):
        import requests

        map_request = f"http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_request, params={'ll': f'{self.line1.text()},{self.line2.text()}',
                                                     'spn': '10,10',
                                                     'l': 'map'})

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        with open('123.png', 'wb') as f:
            f.write(response.content)
        self.pixmap = QPixmap('123.png').scaled(800, 500)
        self.image.setPixmap(self.pixmap)

        self.btn.deleteLater()
        self.line1.deleteLater()
        self.line2.deleteLater()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = FileStat()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
