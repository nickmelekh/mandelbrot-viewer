import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QDesktopWidget, QSlider, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QCoreApplication, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from math import fabs

W, H = 600, 600
size = 100

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(W, H)
        self.center()
        self.setWindowTitle('Donut')

        self.m = PlotCanvas(self)
        self.m.move(-105, -100)

        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(W - 70, H - 40)
        qbtn.setToolTip('You will <b>EXIT</b> the app')

        btn1 = QPushButton('Reset', self)
        btn1.clicked.connect(self.btn1Clicked)
        btn1.resize(qbtn.sizeHint())
        btn1.move(W - 130, H - 40)
        btn1.setToolTip('Print <b>10</b> in command line')

        btn2 = QPushButton('Zoom', self)
        btn2.clicked.connect(self.btn2Clicked)
        btn2.resize(qbtn.sizeHint())
        btn2.move(W - 190, H - 40)

        btn3 = QPushButton('Render', self)
        btn3.clicked.connect(self.btn3Clicked)
        btn3.resize(qbtn.sizeHint())
        btn3.move(W - 590, H - 40)

        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(W - 340, H - 40, 100, 30)
        sld.setMinimum(3)
        sld.setMaximum(20)
        sld.setValue(10)
        sld.valueChanged[int].connect(self.changeValue)

        self.label = QLabel(self)
        self.label.setText(str(im.zoom))
        self.label.setGeometry(W - 230, H - 40, 40, 30)

        sld2 = QSlider(Qt.Horizontal, self)
        sld2.setFocusPolicy(Qt.NoFocus)
        sld2.setGeometry(W - 510, H - 40, 100, 30)
        sld2.setMinimum(100)
        sld2.setMaximum(3000)
        sld2.valueChanged[int].connect(self.changeValue2)

        self.label2 = QLabel(self)
        self.label2.setText(str(im.size))
        self.label2.setGeometry(W - 400, H - 40, 40, 30)

        self.show()

    # def mouseMoveEvent(self, e):
    #     x = e.x()
    #     y = e.y()
    #     print(x, y)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F5:
            self.close()

        if e.key() == Qt.Key_Left:
            im.pmin *= 1.5
            im.pmax = im.len - fabs(im.pmin)
            im.im = im.mandelbrot()
            ex.m.plot()

        if e.key() == Qt.Key_Right:
            im.pmax *= 1.5
            im.pmin = fabs(im.pmax) - im.len
            im.im = im.mandelbrot()
            ex.m.plot()

        if e.key() == Qt.Key_Up:
            im.qmin *= 1.1
            im.qmax = im.hgh - fabs(im.qmin)
            im.im = im.mandelbrot()
            ex.m.plot()

        if e.key() == Qt.Key_Down:
            im.qmin *= 0.9
            im.qmax = im.hgh - fabs(im.qmin)
            im.im = im.mandelbrot()
            ex.m.plot()

    def changeValue(self, value):
        im.zoom = 10/value
        self.label.setText(str(im.zoom))
        print(im.zoom)

    def changeValue2(self, value):
        if value >= 1:
            im.size = value
        self.label2.setText(str(im.size))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def btn1Clicked(self):
        im.pmin = -2.5
        im.pmax = 1.5
        im.qmin = -2
        im.qmax = 2
        im.len = 4
        im.hgh = 4
        im.im = im.mandelbrot()
        ex.m.plot()

    def btn3Clicked(self):
        im.im = im.mandelbrot()
        ex.m.plot()

    def btn2Clicked(self):
        im.pmin *= im.zoom
        im.pmax *= im.zoom
        im.qmin *= im.zoom
        im.qmax *= im.zoom
        im.len *= im.zoom
        im.hgh *= im.zoom
        im.im = im.mandelbrot()
        print(im.zoom)
        ex.m.plot()

class Im(object):
    def __init__(self):
        self.pmin = -2.5
        self.pmax = 1.5
        self.qmin = -2
        self.qmax = 2
        self.size = size
        self.zoom = 1
        self.iter_max = 200
        self.inf_brdr = 10
        self.im = self.mandelbrot()
        self.len = 4
        self.hgh = 4

    def mandelbrot(self):
        print('Computing...')
        p, q = np.mgrid[self.pmin:self.pmax:(self.size * 1j), self.qmin:self.qmax:(self.size * 1j)]
        c = p + 1j * q
        z = np.zeros_like(c)
        mask = 0
        image = np.zeros((self.size, self.size))
        for k in range(self.iter_max):
            z = z ** 2 + c
            mask = (np.abs(z) > self.inf_brdr) & (image == 0)
            image[mask] = k
            z[mask] = np.nan
        im = -image.T
        return im

class PlotCanvas(FigureCanvas):
    def __init__(self, parent = None, width = 8, height = 8, dpi = 100):
        fig = Figure(figsize = (width, height), dpi = dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.imshow(im.im, cmap = 'flag', interpolation = 'none')
        print('Done')
        ax.set_title('Mandelbrot Set')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'icon_1.png')
    app.setWindowIcon(QIcon(path))
    im = Im()
    ex = App()
    ex.setMouseTracking(True)
    sys.exit(app.exec_())
