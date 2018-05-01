from PyQt5.QtWidgets import QMessageBox


def erro_null():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setText("Erro de preenchimento de tabela!")
    msg.setInformativeText("É necessário que todos os campos da tabela estejam preenchidos com valores inteiros"
                           "ou decimais")
    msg.setWindowTitle("Erro de preenchimento")
    msg.setStandardButtons(QMessageBox.Close)

    msg.exec_()


def erro_formato_errado():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setText("Erro de Formato!")
    msg.setInformativeText("O valor a ser inserido precisa ser inteiro")
    msg.setWindowTitle("Erro de formato")
    msg.setStandardButtons(QMessageBox.Close)

    msg.exec_()