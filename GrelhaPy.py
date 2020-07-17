"""Arquivo principal do programa"""
import sys

from PyQt5.QtWidgets import QApplication
from Data.Visual.Janelas import Janelas
from Data.Visual.VisualConfig import VisualConfig
from numpy import array, inf


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


# noinspection PyUnresolvedReferencesicoord = matriz.shape[0]
#             jcoord = matriz.shape[1]
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
        menu_ajuda = main_menu.addMenu('Ajuda')

        menu_ajuda.setEnabled(False)

        ##################################################################################
        # Criação do objeto da classe janelas que irá conter o stack das páginas
        self.Janelas = Janelas()
        self.setCentralWidget(self.Janelas)

        ##################################################################################
        """Definição dos submenus"""
        # Menu de arquivo
        menu_arquivo.addAction(self.Janelas.botao_abrir)
        menu_arquivo.addAction(self.Janelas.botao_novo)
        menu_arquivo.addAction(self.Janelas.botao_salvar)

        # Menu de geometria
        menu_geometria.addAction(self.Janelas.botao_nos)

        # Menu dos módulos de elasticidade
        menu_materiais.addAction(self.Janelas.botao_elasticidade)

        # Menu das forças
        menu_forcas.addAction(self.Janelas.botao_forcas_concentradas)
        menu_forcas.addAction(self.Janelas.botao_forcas_distribuidas)

        # Menu das análises
        menu_analise.addAction(self.Janelas.botao_analise)
        menu_analise.addSeparator()
        menu_analise.addAction(self.Janelas.botao_deslocamentos)
        menu_analise.addAction(self.Janelas.botao_reacoes_apoio)
        menu_analise.addAction(self.Janelas.botao_esi)
        menu_analise.addAction(self.Janelas.botao_matriz)


        # ##################################################################################

        self.setStatusBar(self.Janelas.statusBar)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GrelhaCalcMain()
    sys.exit(app.exec_())

