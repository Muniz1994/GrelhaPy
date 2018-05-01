import sys

from numpy import savez, load

from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction)


from Data.Visual.Janelas import Janelas
from Data.Visual.VisualConfig import VisualConfig

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


# noinspection PyUnresolvedReferences
class GrelhaCalcMain(VisualConfig):

    def __init__(self):
        super().__init__()


        ##################################################################################
        """Criação dos menus"""
        main_menu = self.menuBar()
        menu_arquivo = main_menu.addMenu('Arquivo')
        menu_geometria = main_menu.addMenu('Geometria')
        menu_materiais = main_menu.addMenu('Materiais')
        menu_forcas = main_menu.addMenu('Forças')
        menu_analise = main_menu.addMenu('Análise')

        ##################################################################################
        """Definição dos submenus"""
        # Menu de arquivo
        botao_abrir = QAction('Abrir...', self)
        botao_novo = QAction('Novo', self)
        botao_salvar = QAction('Salvar', self)
        menu_arquivo.addAction(botao_abrir)
        menu_arquivo.addAction(botao_novo)
        menu_arquivo.addAction(botao_salvar)

        # Menu de geometria
        botao_nos = QAction('Nós e Barras', self)
        menu_geometria.addAction(botao_nos)

        # Menu dos módulos de elasticidade
        botao_elasticidade = QAction('Módulos de elasticidade', self)
        menu_materiais.addAction(botao_elasticidade)

        # Menu das forças
        botao_forcas_distribuidas = QAction('Forças Distribuídas', self)
        botao_forcas_concentradas = QAction('Forças Concentradas', self)
        menu_forcas.addAction(botao_forcas_concentradas)
        menu_forcas.addAction(botao_forcas_distribuidas)

        # Menu das análises
        botao_deslocamentos = QAction('Deslocamentos', self)
        botao_reacoes_apoio = QAction('Reações de apoio', self)
        botao_esi = QAction('Esforços solicitantes', self)
        menu_analise.addAction(botao_deslocamentos)
        menu_analise.addAction(botao_reacoes_apoio)
        menu_analise.addAction(botao_esi)

        ##################################################################################
        # Criação do objeto da classe janelas que irá conter o stack das páginas
        self.Janelas = Janelas()
        self.setCentralWidget(self.Janelas)

        ##################################################################################
        # Definição das funções dos botões do submenu
        botao_salvar.triggered.connect(self.save_event)
        botao_abrir.triggered.connect(self.read_event)
        botao_nos.triggered.connect(self.Janelas.botao_nos)
        # botao_barras.triggered.connect(self.Janelas.botao_barras)
        botao_elasticidade.triggered.connect(self.Janelas.botao_elasticidade)
        botao_forcas_distribuidas.triggered.connect(self.Janelas.botao_forcas_distribuidas)
        botao_forcas_concentradas.triggered.connect(self.Janelas.botao_forcas_concentradas)
        botao_deslocamentos.triggered.connect(self.Janelas.botao_deslocamentos)
        botao_reacoes_apoio.triggered.connect(self.Janelas.botao_reacoes_apoio)
        botao_esi.triggered.connect(self.Janelas.botao_esi)

        self.statusbar = self.statusBar()

        self.show()

    def save_event(self):
        global NumeroDeNos, NumeroDeBarras, MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais,\
        CondicoesDeContorno, G, E, J, I

        savez("Savefile.txt", NumeroDeNos)

    def read_event(self):
        global NumeroDeNos, NumeroDeBarras, MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais, \
            CondicoesDeContorno, G, E, J, I

        save_file = load("Savefile.txt")

        print(save_file)

        self.Janelas.edit_text_nos.setText(NumeroDeNos)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GrelhaCalcMain()
    sys.exit(app.exec_())
