"""Arquivo de construção das páginas do programa e métodos para obtenção dos dados da tabela e
apresentação dos resultados"""


from numpy import zeros, around, concatenate, array, inf, isnan

import pandas as pd


from PyQt5.QtWidgets import (QStackedWidget, QWidget,
                             QGridLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget
, QVBoxLayout, QLineEdit, QTableWidgetItem, QTabWidget, QStatusBar, QAction, QCheckBox,
                             QComboBox, QMessageBox, QFileDialog)


from PyQt5.QtCore import Qt
from Data.Analise import Analises
from Data.Erros.Erros import erro_null, erro_formato_errado, erro_aus_dados
import matplotlib.pyplot as pl
from Data.Analise.Estruturas import Grelha
from mpl_toolkits import mplot3d
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Janelas(QWidget):

    def __init__(self):
        super().__init__()

        self.statusBar = QStatusBar()
        self.statusBar.showMessage("Que a força esteja com você!", 2000)

        ##################################################################################
        global NumeroDeNos, NumeroDeBarras, MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais, \
            CondicoesDeContorno, G, E, J, I

        NumeroDeNos = array([inf])
        NumeroDeBarras = array([inf])
        MatrizDeCoordenadas = array([inf])
        MatrizDeConectividade = array([inf])
        ForcasDistribuidas = array([inf])
        ForcasNodais = array([inf])
        CondicoesDeContorno = array([inf])
        G = array([inf])
        E = array([inf])
        J = array([inf])
        I = array([inf])

        ##################################################################################
        """Definição das janelas """
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
        self.matriz_de_rigidez = QWidget()

        self.nost.addTab(self.nos, 'Nós')
        self.nost.addTab(self.barras, 'Barras')
        self.nost.addTab(self.nos_view, 'Estrutura')

        self.nost.setTabEnabled(1, False)
        self.nost.setTabEnabled(2, False)

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
        self.matriz_de_rigidez_ui()

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
        self.Stack.addWidget(self.matriz_de_rigidez)

        ##################################################################################

        vbox = QVBoxLayout()
        vbox.addWidget(self.Stack)

        ##################################################################################
        self.setLayout(vbox)

        """Definição dos submenus"""
        # Menu de arquivo
        self.botao_abrir = QAction('Abrir...', self)
        self.botao_novo = QAction('Novo', self)
        self.botao_salvar = QAction('Salvar', self)

        # Menu de geometria
        self.botao_nos = QAction('Nós e Barras', self)

        # Menu dos módulos de elasticidade
        self.botao_elasticidade = QAction('Módulos de elasticidade', self)

        # Menu das forças
        self.botao_forcas_distribuidas = QAction('Forças Distribuídas', self)
        self.botao_forcas_concentradas = QAction('Forças Concentradas', self)

        # Menu das análises
        self.botao_analise = QAction('Executar análise', self)
        self.botao_deslocamentos = QAction('Deslocamentos', self)
        self.botao_reacoes_apoio = QAction('Reações de apoio', self)
        self.botao_esi = QAction('Esforços solicitantes', self)
        self.botao_matriz = QAction('Matriz de rigidez', self)

        self.botao_deslocamentos.setDisabled(True)
        self.botao_reacoes_apoio.setDisabled(True)
        self.botao_esi.setDisabled(True)
        self.botao_matriz.setDisabled(True)

        ##################################################################################
        # Definição das funções dos botões do submenu
        self.botao_salvar.triggered.connect(self.save_event)
        self.botao_abrir.triggered.connect(self.read_event)
        self.botao_novo.triggered.connect(self.novo_event)
        # Páginas
        self.botao_nos.triggered.connect(lambda: self.Stack.setCurrentIndex(0))
        self.botao_elasticidade.triggered.connect(lambda: self.Stack.setCurrentIndex(1))
        self.botao_forcas_distribuidas.triggered.connect(lambda: self.Stack.setCurrentIndex(2))
        self.botao_forcas_concentradas.triggered.connect(lambda: self.Stack.setCurrentIndex(3))
        self.botao_analise.triggered.connect(self.botao_analise_exec)
        self.botao_deslocamentos.triggered.connect(lambda: self.Stack.setCurrentIndex(4))
        self.botao_reacoes_apoio.triggered.connect(lambda: self.Stack.setCurrentIndex(5))
        self.botao_esi.triggered.connect(lambda: self.Stack.setCurrentIndex(6))
        self.botao_matriz.triggered.connect(lambda: self.Stack.setCurrentIndex(7))

    #######################################################################################
    """Métodos das páginas"""
    def nos_ui(self):
        # Definição dos objetos da página
        text = QLabel('Defina a quantidade de nós:')

        # Caixa de texto para definição dos nós
        self.edit_text_nos = QLineEdit(self)
        self.edit_text_nos.setMaximumSize(180, 50)

        # Botão para definir a quantidade de nós
        botao = QPushButton('Definir', self)
        botao.clicked.connect(self.botao_def_nos)

        # Botão de atualizar as informações da tabela
        self.botao_atualizar_nos = QPushButton('Atualizar', self)
        self.botao_atualizar_nos.setEnabled(False)
        self.botao_atualizar_nos.clicked.connect(self.botao_atualizar_nosm)

        # Tabela
        self.tabela_nos = QTableWidget()
        self.tabela_nos.setColumnCount(5)
        self.tabela_nos.setHorizontalHeaderLabels(("Coordenada X(m)", "Coordenada Y(m)", "Apoio em X",
                                                   "Apoio em Y", "Apoio em Z"))

        #######################################################################################
        # Definição dos layouts da página
        layout = QGridLayout()
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        hlayout.addWidget(self.edit_text_nos)
        hlayout.addWidget(botao)
        hlayout.addStretch()
        hlayout.addWidget(self.botao_atualizar_nos)

        vlayout.addWidget(text)
        vlayout.addLayout(hlayout)

        layout.addLayout(vlayout, 0, 0)
        layout.addWidget(self.tabela_nos, 1, 0)

        self.nos.setLayout(layout)
        #######################################################################################

    def nos_view_ui(self):
        # Tela de apresentação da estrutura
        self.fig = pl.Figure()
        self.ax = mplot3d.Axes3D(self.fig)
        # self.ax.set_axis_off()

        self.canvas = FigureCanvas(self.fig)
        self.ax.mouse_init()

        # Definição dos layouts
        layout = QGridLayout()
        # layout.addWidget(view, 0, 0)
        layout.addWidget(self.canvas, 0, 0)
        # layout.addWidget(self.mpl_toolbar, 1, 0)

        self.nos_view.setLayout(layout)

    def barras_ui(self):
        # Definição dos objetos da página
        text = QLabel('Defina a quantidade de barras:')

        # Caixa de texto para inserção da quantidade de barras
        self.edit_text_barras = QLineEdit()
        self.edit_text_barras.setMaximumSize(180, 50)

        # Botão de definição da quantidade de barras
        botao = QPushButton('Definir')
        botao.clicked.connect(self.botao_def_barras)

        # Botão para atualizar as características das barras
        self.botao_atualizar_barras = QPushButton('Atualizar', self)
        self.botao_atualizar_barras.setEnabled(False)
        self.botao_atualizar_barras.clicked.connect(self.botao_atualizar_barrasm)

        # Criação da tabela
        self.tabela_barras = QTableWidget()
        self.tabela_barras.setColumnCount(4)
        self.tabela_barras.setHorizontalHeaderLabels(
            ("Nó inicial", "Nó final", "Momento de inércia longitudinal (I)", "Momento de inércia Transversal (J)"))
        self.tabela_barras.setColumnWidth(2, 230)
        self.tabela_barras.setColumnWidth(3, 230)

        #######################################################################################
        # Definição do layout da página
        layout = QGridLayout()
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

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
        # Objetos da página
        text = QLabel('Defina os módulos de elasticidade:')

        # Botão para atualizar os dados dos módulos das barras
        botao = QPushButton('Atualizar')
        botao.setMaximumSize(100, 50)
        botao.clicked.connect(self.botao_def_modulos)

        # Criação da tabela
        self.tabela_modulos = QTableWidget()
        self.tabela_modulos.setColumnCount(2)
        self.tabela_modulos.setHorizontalHeaderLabels(
            ("Módulo de elasticidade transversal (G)", "Módulo de elasticidade longitudinal (E)"))
        self.tabela_modulos.setColumnWidth(0, 240)
        self.tabela_modulos.setColumnWidth(1, 240)

        #######################################################################################
        # Definição do layout
        layout = QGridLayout()

        layout.addWidget(text, 0, 0)
        layout.addWidget(self.tabela_modulos, 1, 0)
        layout.addWidget(botao, 2, 0)

        self.modulos.setLayout(layout)

    def forcas_distribuidas_ui(self):
        # Objetos da página
        text = QLabel('Defina as forças distribuídas:')

        # botão de atualizar as informações da tabela
        botao = QPushButton('Atualizar')
        botao.setMaximumSize(100, 50)
        botao.clicked.connect(self.botao_forcas_distribuidas_at)

        # Criação da tabela
        self.tabela_forcas_distribuidas = QTableWidget()
        self.tabela_forcas_distribuidas.setColumnCount(1)
        self.tabela_forcas_distribuidas.setHorizontalHeaderLabels(["Força distribuída KN/m"])
        self.tabela_forcas_distribuidas.setColumnWidth(0, 240)

        #######################################################################################
        # Definição do layout
        layout = QGridLayout()

        layout.addWidget(text, 0, 0)
        layout.addWidget(self.tabela_forcas_distribuidas, 1, 0)
        layout.addWidget(botao, 2, 0)

        self.forcas_distribuidas.setLayout(layout)

    def forcas_concentradas_ui(self):
        # Objetos da página
        text = QLabel('Defina as forças concentradas:')

        # Botão para atualizar as informações da tabela
        botao = QPushButton('Atualizar')
        botao.setMaximumSize(100, 50)
        botao.clicked.connect(self.botao_forcas_concentradas_at)

        # Criação da tabela
        self.tabela_forcas_concentradas = QTableWidget()
        self.tabela_forcas_concentradas.setColumnCount(3)
        self.tabela_forcas_concentradas.setHorizontalHeaderLabels(
            ("Momento em X(KN.m)", "Momento em Y(KN.m)", "Força horizontal em Z(KN)"))
        self.tabela_forcas_concentradas.setColumnWidth(0, 200)
        self.tabela_forcas_concentradas.setColumnWidth(1, 200)
        self.tabela_forcas_concentradas.setColumnWidth(2, 200)

        #######################################################################################
        # Definição do layout
        layout = QGridLayout()

        layout.addWidget(text, 0, 0)
        layout.addWidget(self.tabela_forcas_concentradas, 1, 0)
        layout.addWidget(botao, 2, 0)

        self.forcas_concentradas.setLayout(layout)

    def deslocamentos_ui(self):
        # Objetos da página
        text = QLabel('Deslocamentos:')

        # Criação da tabela
        self.tabela_deslocamentos = QTableWidget()
        self.tabela_deslocamentos.setColumnCount(1)
        self.tabela_deslocamentos.setHorizontalHeaderLabels(["Deslocamentos nodais(m)"])
        self.tabela_deslocamentos.setColumnWidth(0, 200)

        #######################################################################################
        # Definição do layout
        layout = QGridLayout()

        layout.addWidget(text, 0, 0)
        layout.addWidget(self.tabela_deslocamentos, 1, 0)

        self.deslocamentos.setLayout(layout)

    def reacoes_apoio_ui(self):
        # Objetos da página
        text = QLabel('Reações de apoio:')

        # Criação da tabela
        self.tabela_reacoes = QTableWidget()
        self.tabela_reacoes.setColumnCount(3)
        self.tabela_reacoes.setHorizontalHeaderLabels(("Reação em X(KN.m)", "Reação em Y(KN.m)", "Reação em Z(KN)"))
        self.tabela_reacoes.setColumnWidth(0, 160)
        self.tabela_reacoes.setColumnWidth(1, 160)
        self.tabela_reacoes.setColumnWidth(2, 160)

        #######################################################################################
        # Definição do layout
        layout = QGridLayout()

        layout.addWidget(text, 0, 0)
        layout.addWidget(self.tabela_reacoes, 1, 0)

        self.reacoes_apoio.setLayout(layout)

    def esi_ui(self):
        # Objetos da página
        text = QLabel('Esforços solicitantes internos:')

        # Criação da tabela
        self.tabela_esi = QTableWidget()
        self.tabela_esi.setColumnCount(6)
        self.tabela_esi.setHorizontalHeaderLabels(
            ("Esforço inicial em X(KN.m)", "Esforço inicial em Y(KN.m)",
             "Esforço inicial em Z(KN)", "Esforço final em X(KN.m)", "Esforço final em Y(KN.m)",
             "Esforço final em Z(KN)"))
        self.tabela_esi.setColumnWidth(0, 220)
        self.tabela_esi.setColumnWidth(1, 220)
        self.tabela_esi.setColumnWidth(2, 220)
        self.tabela_esi.setColumnWidth(3, 220)
        self.tabela_esi.setColumnWidth(4, 220)
        self.tabela_esi.setColumnWidth(5, 220)

        #######################################################################################
        # Definição do layout
        layout = QGridLayout()

        layout.addWidget(text, 0, 0)
        layout.addWidget(self.tabela_esi, 1, 0)

        self.esi.setLayout(layout)

    def matriz_de_rigidez_ui(self):
        # Objetos da página
        text = QLabel('Matriz de rigidez global:')

        # Criação da tabela
        self.tabela_matriz_rigidez = QTableWidget()

        #######################################################################################
        # Definição do layout
        layout = QGridLayout()

        layout.addWidget(text, 0, 0)
        layout.addWidget(self.tabela_matriz_rigidez, 1, 0)

        self.matriz_de_rigidez.setLayout(layout)

    #######################################################################################
    """Métodos dos botões"""
    def botao_def_nos(self):
        # Recuperação de variável global
        global NumeroDeNos

        # início das operações que necessítam da quantidades de nós da estrutura
        try:
            # Recuperação do valor do número de nós a partir da caixa de edição de texto
            NumeroDeNos = int(self.edit_text_nos.text())

            # Definição do tamanho da tabela em função da quantidade de nós
            self.tabela_nos.setRowCount(NumeroDeNos)

            # Determinação de valores nulos para as restrições dos apoios na tabela
            for j in range(3):
                for i in range(NumeroDeNos):
                    self.tabela_nos.setItem(i, j+2, QTableWidgetItem("0"))

            # Permissão para atualização dos valores da tabela
            self.botao_atualizar_nos.setEnabled(True)

            # Determinação do tamanho da tabela de forças concentradas em função do número de nós
            self.tabela_forcas_concentradas.setRowCount(NumeroDeNos)

            # Determinação de valores nulos para as forças concentradas na tabela
            for j in range(3):
                for i in range(NumeroDeNos):
                    self.tabela_forcas_concentradas.setItem(i, j, QTableWidgetItem("0"))

        except ValueError:
            erro_formato_errado()

    def botao_atualizar_nosm(self):
        # Recuperação de variáveis globais
        global NumeroDeNos, MatrizDeCoordenadas, CondicoesDeContorno


        # Determinação das variáveis como matrizes zeradas
        if inf in MatrizDeCoordenadas.tolist():
            MatrizDeCoordenadas = zeros((NumeroDeNos, 2))

        if inf in CondicoesDeContorno.tolist():
            CondicoesDeContorno = zeros((NumeroDeNos, 3))

        # Recuperação dos valores da tabela e inserção nas matrizes
        try:
            for i in range(NumeroDeNos):
                for j in range(2):
                    MatrizDeCoordenadas[i, j] = float(self.tabela_nos.item(i, j).text())
                for j in range(3):
                    CondicoesDeContorno[i, j] = int(self.tabela_nos.item(i, j+2).text())
        except ValueError:
            erro_null()

        self.ax.clear()
        self.ax.mouse_init()
        for no, coord in enumerate(MatrizDeCoordenadas):
            self.ax.scatter(coord[0], coord[1], 0, color='black')
            self.ax.text(coord[0], coord[1], 0, 'nó {} ({},{})'.format((no+1), coord[0], coord[1]))

        self.nost.setTabEnabled(1, True)

        self.statusBar.showMessage('Informações dos nós atualizadas!', 2500)

    def botao_def_barras(self):
        # Recuperação de variável global
        global NumeroDeBarras
        try:
            # Atribuição de valor da caixa de texto para variável do número de barras
            NumeroDeBarras = int(self.edit_text_barras.text())

            # Definição da quantidade de linhas da tabela de barras em função do número de barras
            self.tabela_barras.setRowCount(NumeroDeBarras)

            # Dimensionamento da tabela de módulos em função do número de barras
            self.tabela_modulos.setRowCount(NumeroDeBarras)

            # Dimensionamento da tabela de forças distribuídas em função do número de barras
            self.tabela_forcas_distribuidas.setRowCount(NumeroDeBarras)

            # Permissão para atualização das informações da tabela de barras
            self.botao_atualizar_barras.setEnabled(True)

            # Determinação de valores zerados para a tabela de forças distribuídas
            for i in range(NumeroDeBarras):
                self.tabela_forcas_distribuidas.setItem(i, 0, QTableWidgetItem("0"))

        except ValueError:
            erro_formato_errado()

    def botao_atualizar_barrasm(self):
        # Recuperação de variáveis globais
        global NumeroDeBarras, MatrizDeConectividade, J, I, MatrizDeCoordenadas

        # Atribuição de valores nulos às variáveis
        if inf in MatrizDeConectividade.tolist():
            MatrizDeConectividade = zeros((NumeroDeBarras, 2))

        if inf in J.tolist():
            J = zeros((NumeroDeBarras, 1))

        if inf in I.tolist():
            I = zeros((NumeroDeBarras, 1))

        try:
            # Recuperação dos valores da tabela para inserção nas matrizes zeradas
            for i in range(NumeroDeBarras):
                for j in range(2):
                    MatrizDeConectividade[i, j] = int(self.tabela_barras.item(i, j).text())

                J[i, 0] = float(self.tabela_barras.item(i, 2).text())
                I[i, 0] = float(self.tabela_barras.item(i, 3).text())
        except ValueError:
            erro_null()

        for nbarras, conectividade in enumerate(MatrizDeConectividade):
            varx = (MatrizDeCoordenadas[int(conectividade[0])-1, 0], MatrizDeCoordenadas[int(conectividade[1])-1, 0])
            vary = (MatrizDeCoordenadas[int(conectividade[0])-1, 1], MatrizDeCoordenadas[int(conectividade[1])-1, 1])

            line = mplot3d.art3d.Line3D(varx, vary, (0, 0), c='green', linewidth=3)

            self.ax.add_line(line)
        # Status de informações atualizadas
        self.statusBar.showMessage('Informações das barras atualizadas!', 2500)

    def botão_atualizar_apoios(self):
        global CondicoesDeContorno, NumeroDeNos

        if inf in CondicoesDeContorno.tolist():
            CondicoesDeContorno = zeros(NumeroDeNos, 3)

    def botao_def_modulos(self):
        # Recuperação de variáveis globais
        global NumeroDeBarras, G, E

        # Atribuição de matriz com valores nulos às variáveis
        if inf in G.tolist():
            G = zeros((NumeroDeBarras, 1))

        if inf in E.tolist():
            E = zeros((NumeroDeBarras, 1))

        try:
            # Recuperação dos valores da tabela e inserção
            for i in range(NumeroDeBarras):

                G[i, 0] = float(self.tabela_modulos.item(i, 0).text())
                E[i, 0] = float(self.tabela_modulos.item(i, 1).text())
        except:
            erro_null()

        self.statusBar.showMessage('Módulos atualizados!', 2500)

    def botao_forcas_distribuidas_at(self):
        # Recuperação das variáveis globais
        global ForcasDistribuidas, NumeroDeBarras

        # Atribuição de matrizes de valores nulos às variáveis
        if inf in ForcasDistribuidas.tolist():
            ForcasDistribuidas = zeros((NumeroDeBarras, 1))
        print(ForcasDistribuidas)
        print(NumeroDeBarras)
        try:
            # Recuperação dos valores da tabela e inserção nas matrizes zeradas
            for i in range(NumeroDeBarras):

                ForcasDistribuidas[i, 0] = int(self.tabela_forcas_distribuidas.item(i, 0).text())
        except:
            erro_null()

        self.statusBar.showMessage('Forças distribuídas atualizadas!', 2500)

    def botao_forcas_concentradas_at(self):
        # Recuperação das variáveis globais
        global NumeroDeNos, ForcasNodais

    # Atribuição de matriz zerada à variável
        if inf in ForcasNodais.tolist():
            ForcasNodais = zeros((NumeroDeNos, 3))

        try:
            # Recuperação dos valores da tabela e inserção na matriz zerada
            for i in range(NumeroDeNos):
                for j in range(3):
                    ForcasNodais[i, j] = int(self.tabela_forcas_concentradas.item(i, j).text())
        except:
            erro_null()

        self.statusBar.showMessage('Forças concentradas atualizadas!', 2500)

        print(ForcasNodais)

    #######################################################################################
    def botao_analise_exec(self):
        # Recuperação das variáveis globais
        global NumeroDeNos, NumeroDeBarras, MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, \
            ForcasNodais, CondicoesDeContorno, G, E, J, I

        # Execução da pré-análise, com definição das variáveis
        try:
            R = Analises.Analise(
                Grelha(MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais,
                                CondicoesDeContorno, G, E, J, I))

            # Cálculo dos deslocamentos
            D = R.linear_elastica()

            # Dimensionamento da tabela de deslocamentos em função da quantidade de nós
            self.tabela_deslocamentos.setRowCount(NumeroDeNos * 3)

            # Atribuição dos resultados à tabela
            for i in range(NumeroDeNos * 3):
                self.tabela_deslocamentos.setItem(i, 0, QTableWidgetItem(str("{0:1.4E}".format(D[i, 0]))))

            #######################################################################################

            # Cálculo das reações de apoio
            reacoes = R.reacoes_apoio()

            # Dimensionamento da tabela em função do número de nós
            self.tabela_reacoes.setRowCount(NumeroDeNos)

            # Inserção dos valores dos resultados nas tabelas
            for i in range(NumeroDeNos):
                for j in range(3):
                    if abs(reacoes[i, j]) >= 0.0001:
                        self.tabela_reacoes.setItem(i, j, QTableWidgetItem(str(around(reacoes[i, j], 4))))
                    else:
                        self.tabela_reacoes.setItem(i, j, QTableWidgetItem("0.0"))
            self.tabela_reacoes.setDisabled(False)

            #######################################################################################

            # Cálculo dos esforços solicitantes
            esi = R.eforcos_solicitantes()

            # Dimensionamento da tabela em função do número de barras
            self.tabela_esi.setRowCount(NumeroDeBarras)

            # Inserção dos valores dos resultados na tabela
            for j in range(6):
                for i in range(NumeroDeBarras):
                    if abs(esi[i, j]) >= 0.0001:
                        self.tabela_esi.setItem(i, j, QTableWidgetItem(str(around(esi[i, j], 4))))
                    else:
                        self.tabela_esi.setItem(i, j, QTableWidgetItem("0.0"))

            #######################################################################################

            # apresentação da matriz de rigidez
            matrizderigidez = R.MatrizRigidezGlobal

            # Dimensionamento da tabela em função do número de nós
            self.tabela_matriz_rigidez.setRowCount(3*NumeroDeNos)
            self.tabela_matriz_rigidez.setColumnCount(3*NumeroDeNos)

            # Inserção dos valores dos resultados na tabela
            for j in range(3*NumeroDeNos):
                for i in range(3*NumeroDeNos):
                    self.tabela_matriz_rigidez.setItem(i, j, QTableWidgetItem(str("{0:1.4E}".format(matrizderigidez[i, j]))))

            self.botao_deslocamentos.setDisabled(False)
            self.botao_reacoes_apoio.setDisabled(False)
            self.botao_esi.setDisabled(False)
            self.botao_matriz.setDisabled(False)

        except NameError:
            erro_aus_dados()

    #######################################################################################
    """Métodos de arquivo"""
    def save_event(self):
        global NumeroDeNos, NumeroDeBarras, MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas,\
            ForcasNodais, CondicoesDeContorno, G, E, J, I

        file = QFileDialog.getSaveFileName(self, "Salve o projeto", "", "Excel file (*.xlsx)")

        save = pd.ExcelWriter(file[0], engine='xlsxwriter')

        if MatrizDeCoordenadas.any() and CondicoesDeContorno.any():
            matrizCoord = pd.DataFrame(data=MatrizDeCoordenadas, columns=['coord x', 'coord y'])

            condContorno = pd.DataFrame(data=CondicoesDeContorno, columns=['Apoio em x', 'Apoio em y', 'Apoio em z'])

            matrizCoord.to_excel(save, sheet_name='Matriz de coordenadas')

            condContorno.to_excel(save, sheet_name='Condições de contorno')

        if MatrizDeConectividade.any() and J.any() and I.any():
            matrizConect = pd.DataFrame(data=MatrizDeConectividade, columns=['Nó 1', 'Nó 2'])

            inerciaT = pd.DataFrame(data=J, columns=['J'])

            inercia = pd.DataFrame(data=I, columns=['I'])

            matrizConect.to_excel(save, sheet_name='Matriz de conectividade')

            inerciaT.to_excel(save, sheet_name='J')

            inercia.to_excel(save, sheet_name='I')

        if ForcasDistribuidas.any():
            forcDist = pd.DataFrame(data=ForcasDistribuidas, columns=['Forças Distribuídas'])

            forcDist.to_excel(save, sheet_name='Forças Distribuídas')

        if ForcasNodais.any():
            forcNod = pd.DataFrame(data=ForcasNodais, columns=['Forças Nodais'])

            forcNod.to_excel(save, sheet_name='Forças Nodais')

        if E.any() and G.any():
            moduloEl1 = pd.DataFrame(data=E, columns=['Módulo de elasticidade'])

            moduloEl1.to_excel(save, sheet_name='E')

            moduloEl2 = pd.DataFrame(data=G, columns=['Módulo de elasticidade'])

            moduloEl2.to_excel(save, sheet_name='G')

        save.save()

    def read_event(self):
        global NumeroDeNos, NumeroDeBarras, MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais, \
            CondicoesDeContorno, G, E, J, I


        open = QFileDialog.getOpenFileName(self, "Abra um projeto", "", "Excel file (*.xlsx)")

        excelF = pd.ExcelFile(open[0])

        sheets = excelF.sheet_names

        print(sheets)

        if 'Matriz de coordenadas' in sheets and 'Condições de contorno' in sheets:
            MatrizDeCoordenadas = pd.read_excel(excelF, 'Matriz de coordenadas',index_col=0 ).to_numpy()

            NumeroDeNos = MatrizDeCoordenadas.shape[0]

            CondicoesDeContorno = pd.read_excel(excelF, 'Condições de contorno',index_col=0).to_numpy()

            self.atualizar_tabela([MatrizDeCoordenadas, CondicoesDeContorno], self.tabela_nos)

            self.tabela_forcas_concentradas.setRowCount(MatrizDeCoordenadas.shape[0])

            self.nost.setTabEnabled(1, True)

            self.botao_atualizar_nos.setEnabled(True)

            # Determinação de valores nulos para as forças concentradas na tabela
            for j in range(3):
                for i in range(NumeroDeNos):
                    self.tabela_forcas_concentradas.setItem(i, j, QTableWidgetItem("0"))


        if 'Matriz de conectividade' in sheets and 'J' in sheets and 'I' in sheets:
            MatrizDeConectividade = pd.read_excel(excelF, 'Matriz de conectividade',index_col=0).to_numpy()

            NumeroDeBarras = MatrizDeConectividade.shape[0]

            J = pd.read_excel(excelF, 'J',index_col=0).to_numpy()

            I = pd.read_excel(excelF, 'I',index_col=0).to_numpy()

            self.atualizar_tabela([MatrizDeConectividade, J, I], self.tabela_barras)

            self.tabela_forcas_distribuidas.setRowCount(MatrizDeConectividade.shape[0])

            self.nost.setTabEnabled(2, True)

            self.botao_atualizar_barras.setEnabled(True)

            # Determinação de valores zerados para a tabela de forças distribuídas
            for i in range(NumeroDeBarras):
                self.tabela_forcas_distribuidas.setItem(i, 0, QTableWidgetItem("0"))

        if 'Forças Distribuídas' in sheets:
            ForcasDistribuidas =  pd.read_excel(excelF, 'Forças Distribuídas',index_col=0).to_numpy()

            self.atualizar_tabela([ForcasDistribuidas], self.tabela_forcas_distribuidas)

        if 'Forças Nodais' in sheets:
            ForcasNodais = pd.read_excel(excelF, 'Forças Nodais',index_col=0).to_numpy()

            self.atualizar_tabela([ForcasNodais], self.tabela_forcas_concentradas)

        if 'E' in sheets and 'G' in sheets:
            E = pd.read_excel(excelF, 'E',index_col=0).to_numpy()

            G = pd.read_excel(excelF, 'G',index_col=0).to_numpy()

            self.atualizar_tabela([E, G], self.tabela_modulos)

        # print(MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais,
        # CondicoesDeContorno, G, E, J, I)


        self.Stack.setCurrentIndex(0)
        self.nost.setCurrentIndex(0)

    def novo_event(self):
        global NumeroDeNos, NumeroDeBarras, MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais, \
            CondicoesDeContorno, G, E, J, I

        novo_msg = "Deseja iniciar uma nova estrutura?"

        resposta = QMessageBox.question(self, 'Nova estrutura',
                    novo_msg, QMessageBox.Yes, QMessageBox.No)

        if resposta == QMessageBox.Yes:
            self.statusBar.showMessage("Novo arquivo!", 3000)

            self.tabela_matriz_rigidez.clearContents()
            self.tabela_matriz_rigidez.setColumnCount(0)
            self.tabela_matriz_rigidez.setRowCount(0)

            self.tabela_reacoes.clearContents()
            self.tabela_reacoes.setRowCount(0)

            self.tabela_deslocamentos.clearContents()
            self.tabela_deslocamentos.setRowCount(0)

            self.tabela_forcas_distribuidas.clearContents()
            self.tabela_forcas_distribuidas.setRowCount(0)

            self.tabela_forcas_concentradas.clearContents()
            self.tabela_forcas_concentradas.setRowCount(0)

            self.tabela_barras.clearContents()
            self.tabela_barras.setRowCount(0)

            self.tabela_nos.clearContents()
            self.tabela_nos.setRowCount(0)

            self.tabela_esi.clearContents()
            self.tabela_esi.setRowCount(0)

            self.tabela_modulos.clearContents()
            self.tabela_modulos.setRowCount(0)

            self.edit_text_barras.clear()

            self.edit_text_nos.clear()

            self.ax.clear()
            self.ax.mouse_init()

            self.botao_deslocamentos.setDisabled(True)
            self.botao_reacoes_apoio.setDisabled(True)
            self.botao_esi.setDisabled(True)
            self.botao_matriz.setDisabled(True)
            self.nost.setTabEnabled(1, False)

            self.Stack.setCurrentIndex(0)
            self.nost.setCurrentIndex(0)

            NumeroDeNos = None
            NumeroDeBarras = None
            MatrizDeCoordenadas = None
            MatrizDeConectividade = None
            ForcasDistribuidas = None
            ForcasNodais = None
            CondicoesDeContorno = None
            G = None
            E = None
            J = None
            I = None
        else:
            pass

    #######################################################################################
    """Métodos auxiliares"""

    def atualizar_tabela (self, matriz, tabela):

        if len(matriz) > 1:
            matriz = concatenate(matriz, axis=1)
            tabela.setRowCount(matriz.shape[0])
            tabela.setColumnCount(matriz.shape[1])
            icoord = matriz.shape[0]
            jcoord = matriz.shape[1]
        else:
            matriz = matriz
            tabela.setRowCount(matriz[0].shape[0])
            tabela.setColumnCount(matriz[0].shape[1])
            icoord = matriz[0].shape[0]
            jcoord = matriz[0].shape[1]



        for i in range(icoord):
            for j in range(jcoord):
                tabela.setItem(i, j, QTableWidgetItem(str(matriz[i, j])))



