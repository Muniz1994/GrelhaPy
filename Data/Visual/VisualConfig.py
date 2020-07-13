from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon
from PyQt5.QtCore import Qt, QSize

class VisualConfig(QMainWindow):

    def __init__(self):
        super().__init__()

        ##################################################################################
        """Características básicas da tela principal"""
        self.setWindowTitle('GrelhaPy')
        self.setGeometry(50, 50, 800, 600)
        self.setMaximumSize(1280, 768)
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(r"C:\\Users\\bruno\\Documents\\Oficial\\6. Gpy\\GrelhaPy\\Gpyicon.png"))

        ##################################################################################
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        ##################################################################################
        import ctypes
        myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

