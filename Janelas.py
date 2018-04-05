from numpy import zeros

from PyQt5.QtWidgets import ( QStackedWidget, QWidget,
                             QGridLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget
                             , QVBoxLayout, QLineEdit, QTableWidgetItem, QTabWidget)


from Grelhapy import Analises
from Grelhapy.Erros import erro_formato_errado, erro_null

import matplotlib.pyplot as pl
import matplotlib.patches as patches
from matplotlib.path import Path

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


# noinspection PyArgumentList,PyUnresolvedReferences,PyAttributeOutsideInit
class Janelas(QWidget):

    def __init__(self):
        super().__init__()

        ##################################################################################
        # Criação das páginas
        self.nost = QTabWidget()
        self.nos = QWidget()
        self.nos_view = QWidget()
        self.barras = QWidget()
        self.modulos = QWidget()
        self.forcas_distribuidas = QWidget()
        self.forcas_concentradas = QWidget()
        self.deslocamentos = QWidget()
        self.reacoes_apoio = QWidget()
        self.esi = QWidget()

        self.nost.addTab(self.nos, 'Nós')
        self.nost.addTab(self.barras, 'Barras')
        self.nost.addTab(self.nos_view, 'Estrutura')

        ##################################################################################
        """Inicialização dos métodos das páginas"""
        self.nos_ui()
        self.nos_view_ui()
        self.barras_ui()
        self.modulos_ui()
        self.forcas_distribuidas_ui()
        self.forcas_concentradas_ui()
        self.deslocamentos_ui()
        self.reacoes_apoio_ui()
        self.esi_ui()

        ##################################################################################
        """Inserção das páginas no stack"""
        self.Stack = QStackedWidget()
        self.Stack.addWidget(self.nost)
        self.Stack.addWidget(self.modulos)
        self.Stack.addWidget(self.forcas_distribuidas)
        self.Stack.addWidget(self.forcas_concentradas)
        self.Stack.addWidget(self.deslocamentos)
        self.Stack.addWidget(self.reacoes_apoio)
        self.Stack.addWidget(self.esi)

        ##################################################################################

        hbox = QHBoxLayout()
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)

    #######################################################################################
    def nos_ui(self):
        layout = QGridLayout()
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        text = QLabel('Defina a quantidade de nós:')

        self.edit_text_nos = QLineEdit(self)
        self.edit_text_nos.setMaximumSize(180, 50)

        botao = QPushButton('Definir', self)
        self.botao_atualizar_nos = QPushButton('Atualizar', self)
        self.botao_atualizar_nos.setEnabled(False)
        self.tabela_nos = QTableWidget()

        botao.clicked.connect(self.botao_def_nos)
        self.botao_atualizar_nos.clicked.connect(self.botao_atualizar_nosm)

        hlayout.addWidget(self.edit_text_nos)
        hlayout.addWidget(botao)
        hlayout.addStretch()
        hlayout.addWidget(self.botao_atualizar_nos)

        vlayout.addWidget(text)
        vlayout.addLayout(hlayout)

        layout.addLayout(vlayout, 0, 0)
        layout.addWidget(self.tabela_nos, 1, 0)

        self.nos.setLayout(layout)

    def nos_view_ui(self):
        layout = QGridLayout()

        self.fig, self.ax = pl.subplots()
        self.canvas = FigureCanvas(self.fig)
        pl.subplots_adjust(left=0, bottom=0, right=1, top=1)
        self.ax.grid()
        self.ax.axis('equal')
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.nos)

        layout.addWidget(self.canvas, 0, 0)
        layout.addWidget(self.mpl_toolbar, 1, 0)

        self.nos_view.setLayout(layout)

    def barras_ui(self):
        layout = QGridLayout()
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        text = QLabel('Defina a quantidade de barras:')

        self.edit_text_barras = QLineEdit()
        self.edit_text_barras.setMaximumSize(180, 50)

        botao = QPushButton('Definir')
        self.botao_atualizar_barras = QPushButton('Atualizar', self)
        self.botao_atualizar_barras.setEnabled(False)
        self.tabela_barras = QTableWidget()

        botao.clicked.connect(self.botao_def_barras)
        self.botao_atualizar_barras.clicked.connect(self.botao_atualizar_barrasm)

        hlayout.addWidget(self.edit_text_barras)
        hlayout.addWidget(botao)
        hlayout.addStretch()
        hlayout.addWidget(self.botao_atualizar_barras)

        vlayout.addWidget(text)
        vlayout.addLayout(hlayout)

        layout.addLayout(vlayout, 0, 0)
        layout.addWidget(self.tabela_barras, 1, 0)

        self.barras.setLayout(layout)

    def modulos_ui(self):
        layout = QGridLayout()

        text = QLabel('Defina os módulos de elasticidade:')
        botao = QPushButton('Atualizar')
        botao.setMaximumSize(100, 50)
        self.tabela_modulos = QTableWidget()

        botao.clicked.connect(self.botao_def_modulos)

        layout.addWidget(text, 0, 0)
        layout.addWidget(self.tabela_modulos, 1, 0)
        layout.addWidget(botao, 2, 0)

        self.modulos.setLayout(layout)

    def forcas_distribuidas_ui(self):
        layout = QGridLayout()

        text = QLabel('Defina as forças distribuídas:')
        botao = QPushButton('Atualizar')
        botao.setMaximumSize(100, 50)
        self.tabela_forcas_distribuidas = QTableWidget()

        botao.clicked.connect(self.botao_forcas_distribuidas_at)

        layout.addWidget(text, 0, 0)
        layout.addWidget(self.tabela_forcas_distribuidas, 1, 0)
        layout.addWidget(botao, 2, 0)

        self.forcas_distribuidas.setLayout(layout)

    def forcas_concentradas_ui(self):
        layout = QGridLayout()

        text = QLabel('Defina as forças concentradas:')
        botao = QPushButton('Atualizar')
        botao.setMaximumSize(100, 50)
        self.tabela_forcas_concentradas = QTableWidget()

        botao.clicked.connect(self.botao_forcas_concentradas_at)

        layout.addWidget(text, 0, 0)
        layout.addWidget(self.tabela_forcas_concentradas, 1, 0)
        layout.addWidget(botao, 2, 0)

        self.forcas_concentradas.setLayout(layout)

    def deslocamentos_ui(self):
        layout = QGridLayout()

        text = QLabel('Deslocamentos:')
        botao = QPushButton("Determinar Deslocamentos")
        botao.setMaximumSize(180, 50)
        self.tabela_deslocamentos = QTableWidget()

        botao.clicked.connect(self.botao_analise_deslocamentos)

        layout.addWidget(text, 0, 0)
        layout.addWidget(self.tabela_deslocamentos, 1, 0)
        layout.addWidget(botao, 2, 0)

        self.deslocamentos.setLayout(layout)

    def reacoes_apoio_ui(self):
        layout = QGridLayout()

        text = QLabel('Reações de apoio:')
        botao = QPushButton("Determinar Reações")
        botao.setMaximumSize(180, 50)
        self.tabela_reacoes = QTableWidget()

        botao.clicked.connect(self.botao_analise_reacoes)

        layout.addWidget(text, 0, 0)
        layout.addWidget(self.tabela_reacoes, 1, 0)
        layout.addWidget(botao, 2, 0)

        self.reacoes_apoio.setLayout(layout)

    def esi_ui(self):
        layout = QGridLayout()

        text = QLabel('Esforços solicitantes internos:')
        botao = QPushButton("Determinar Esforços")
        botao.setMaximumSize(180, 50)
        self.tabela_esi = QTableWidget()

        botao.clicked.connect(self.botao_analise_esi)

        layout.addWidget(text, 0, 0)
        layout.addWidget(self.tabela_esi, 1, 0)
        layout.addWidget(botao, 2, 0)

        self.esi.setLayout(layout)

    #######################################################################################
    def botao_nos(self):

        self.Stack.setCurrentIndex(0)

    # def botao_barras(self):
    #     self.Stack.setCurrentIndex(1)

    def botao_elasticidade(self):
        self.Stack.setCurrentIndex(1)

    def botao_forcas_distribuidas(self):
        self.Stack.setCurrentIndex(2)

    def botao_forcas_concentradas(self):
        self.Stack.setCurrentIndex(3)

    def botao_deslocamentos(self):
        self.Stack.setCurrentIndex(4)

    def botao_reacoes_apoio(self):
        self.Stack.setCurrentIndex(5)

    def botao_esi(self):
        self.Stack.setCurrentIndex(6)

    #######################################################################################
    def botao_def_nos(self):
        global NumeroDeNos
        try:
            NumeroDeNos = int(self.edit_text_nos.text())

            self.botao_atualizar_nos.setEnabled(True)

            self.tabela_nos.setColumnCount(5)
            self.tabela_nos.setRowCount(NumeroDeNos)

            self.tabela_forcas_concentradas.setColumnCount(3)
            self.tabela_forcas_concentradas.setRowCount(NumeroDeNos)
        except:
            erro_formato_errado()

    def botao_atualizar_nosm(self):
        global NumeroDeNos, MatrizDeCoordenadas, CondicoesDeContorno

        MatrizDeCoordenadas = zeros((NumeroDeNos, 2))
        CondicoesDeContorno = zeros((NumeroDeNos, 3))
        try:
            for i in range(NumeroDeNos):
                for j in range(2):
                    MatrizDeCoordenadas[i, j] = float(self.tabela_nos.item(i, j).text())
                for j in range(3):
                    CondicoesDeContorno[i, j] = int(self.tabela_nos.item(i, j+2).text())
        except:
            erro_null()
        self.ax.clear()
        self.ax.grid()
        for i, j in MatrizDeCoordenadas:
            self.ax.plot(i, j, 'go-')
            self.canvas.draw()

    def botao_def_barras(self):
        global NumeroDeBarras
        try:
            NumeroDeBarras = int(self.edit_text_barras.text())

            self.botao_atualizar_barras.setEnabled(True)

            self.tabela_barras.setColumnCount(4)
            self.tabela_barras.setRowCount(NumeroDeBarras)

            self.tabela_modulos.setColumnCount(2)
            self.tabela_modulos.setRowCount(NumeroDeBarras)

            self.tabela_forcas_distribuidas.setColumnCount(1)
            self.tabela_forcas_distribuidas.setRowCount(NumeroDeBarras)
        except:
            erro_formato_errado()

    def botao_atualizar_barrasm(self):
        global NumeroDeBarras, MatrizDeConectividade, J, I, MatrizDeCoordenadas

        MatrizDeConectividade = zeros((NumeroDeBarras, 2))
        J = zeros((NumeroDeBarras, 1))
        I = zeros((NumeroDeBarras, 1))

        try:
            for i in range(NumeroDeBarras):
                for j in range(2):
                    MatrizDeConectividade[i, j] = int(self.tabela_barras.item(i, j).text())

                J[i, 0] = float(self.tabela_barras.item(i, 2).text())
                I[i, 0] = float(self.tabela_barras.item(i, 3).text())
        except ValueError:
            erro_null()
        self.ax.clear()
        self.ax.grid()
        self.botao_atualizar_nosm()
        for i in MatrizDeConectividade:
            diretriz = zeros((2, 2))
            indice = 0
            for j in i:
                diretriz[indice, :] = MatrizDeCoordenadas[int(j - 1), :]
                indice += 1
            path = Path(diretriz, [Path.MOVETO, Path.LINETO])
            patch3 = patches.PathPatch(path, facecolor='white', lw=2)
            self.ax.add_patch(patch3)
            self.canvas.draw()

    def botao_def_modulos(self):
        global NumeroDeBarras, G, E

        G = zeros((NumeroDeBarras, 1))
        E = zeros((NumeroDeBarras, 1))
        try:
            for i in range(NumeroDeBarras):

                G[i, 0] = float(self.tabela_modulos.item(i, 0).text())
                E[i, 0] = float(self.tabela_modulos.item(i, 1).text())
        except:
            erro_null()

    def botao_forcas_distribuidas_at(self):
        global ForcasDistribuidas, NumeroDeBarras

        ForcasDistribuidas = zeros((NumeroDeBarras, 1))
        try:
            for i in range(NumeroDeBarras):

                ForcasDistribuidas[i, 0] = int(self.tabela_forcas_distribuidas.item(i, 0).text())
        except:
            erro_null()

    def botao_forcas_concentradas_at(self):
        global NumeroDeNos, ForcasNodais

        ForcasNodais = zeros((NumeroDeNos, 3))
        try:
            for i in range(NumeroDeNos):
                for j in range(3):
                    ForcasNodais[i, j] = int(self.tabela_forcas_concentradas.item(i, j).text())
        except:
            erro_null()

    def botao_analise_deslocamentos(self):
        global NumeroDeNos, NumeroDeBarras, MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais,\
    CondicoesDeContorno, G, E, J, I

        R = Analises.Analise(Analises.Grelha(MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais,
                           CondicoesDeContorno, G, E, J, I))
        R.linear_elastica()
        D = R.linear_elastica()
        self.tabela_deslocamentos.setColumnCount(1)
        self.tabela_deslocamentos.setRowCount(NumeroDeNos * 3)

        for i in range(NumeroDeNos*3):
            self.tabela_deslocamentos.setItem(i, 0, QTableWidgetItem(str(D[i, 0])))

    def botao_analise_reacoes(self):
        global NumeroDeNos, NumeroDeBarras, MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais,\
    CondicoesDeContorno, G, E, J, I

        R = Analises.Analise(Analises.Grelha(MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais,
                           CondicoesDeContorno, G, E, J, I))

        Reacoes = R.reacoes_apoio()
        self.tabela_reacoes.setColumnCount(3)
        self.tabela_reacoes.setRowCount(NumeroDeNos)

        for i in range(NumeroDeNos):
            for j in range(3):
                self.tabela_reacoes.setItem(i, j, QTableWidgetItem(str(Reacoes[i, j])))

    def botao_analise_esi(self):
        global NumeroDeNos, NumeroDeBarras, MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais,\
    CondicoesDeContorno, G, E, J, I

        R = Analises.Analise(Analises.Grelha(MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais,
                           CondicoesDeContorno, G, E, J, I))

        esi = R.eforcos_solicitantes()
        self.tabela_esi.setColumnCount(6)
        self.tabela_esi.setRowCount(NumeroDeBarras)

        for j in range(6):
            for i in range(NumeroDeBarras):
                self.tabela_esi.setItem(i, j, QTableWidgetItem(str(esi[i, j])))