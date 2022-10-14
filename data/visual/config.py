"""Arquivo para configurações visuais da interface do programa"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class VisualConfig(QMainWindow):

    def __init__(self):
        super().__init__()

        ##################################################################################
        """Características básicas da tela principal"""
        self.setWindowTitle('GrelhaPy - Programa para análise estrutural de grelhas')
        self.setGeometry(50, 50, 800, 600)
        # self.setMaximumSize(1280, 768)
        self.setMinimumSize(800, 600)
        self.move

        icon = QIcon(r"Gpyicon.png")
        self.setWindowIcon(icon)

        ##################################################################################
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        ##################################################################################

        import ctypes
        myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

