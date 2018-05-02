from numpy import dot, zeros, array

from numpy.linalg import inv

from copy import copy

from Data.Analise.Estruturas import Grelha


# Variável a ser modificada


#


# Vetor de forças nodais equivalentes
class Analise:

    def __init__(self, Estrutura):

        self.estrutura = Estrutura
        self.MatrizRigidezGlobal = None
        self.ForcasNodaisEquivalentes = None

    def linear_elastica(self):

        #################################################################################
        """Criação do vetor de forças"""
        self.ForcasNodaisEquivalentes = zeros((self.estrutura.Deslocabilidades * self.estrutura.NumeroDeNos, 1))

        for i in range(1, self.estrutura.NumeroDeBarras+1):

            EngastamentoPerfeitoGlobal = dot(self.estrutura.matriz_rotacao(i).T,
                                             self.estrutura.engastamento_perfeito(i))

            VetorCorrespondenciaIndex = self.estrutura.vetor_correspondencia(i)

            for j in range(1, (2*self.estrutura.Deslocabilidades)+1):

                self.ForcasNodaisEquivalentes[int((VetorCorrespondenciaIndex[j-1, 0])-1), 0]\
                    -= EngastamentoPerfeitoGlobal[j-1, 0]

        self.ForcasNodaisCombinadas = copy(self.ForcasNodaisEquivalentes)

        for i in range(1, self.estrutura.NumeroDeNos+1):

            for j in range(1, self.estrutura.Deslocabilidades+1):

                self.ForcasNodaisCombinadas[(((i-1)*self.estrutura.Deslocabilidades) + j)-1, 0] \
                    += self.estrutura.ForcasNodais[i-1, j-1]

        self.ForcasNodaisNumeroGrande = zeros((self.estrutura.Deslocabilidades * self.estrutura.NumeroDeNos, 1))
        for i in range(1, self.estrutura.NumeroDeNos + 1):
            for j in range(1, self.estrutura.Deslocabilidades + 1):
                if self.estrutura.CondicoesDeContorno[i - 1, j - 1] == 1:
                    self.ForcasNodaisNumeroGrande[(self.estrutura.Deslocabilidades * (i - 1) + j) - 1, 0] = \
                        self.ForcasNodaisCombinadas[(self.estrutura.Deslocabilidades * (i - 1) + j) - 1, 0] + \
                        self.estrutura.NumeroGrande * self.estrutura.DeslocamentosPrescritos[i - 1, j - 1]
                else:
                    self.ForcasNodaisNumeroGrande[(self.estrutura.Deslocabilidades * (i - 1) + j) - 1, 0] = \
                        self.ForcasNodaisCombinadas[(self.estrutura.Deslocabilidades * (i - 1) + j) - 1, 0]

        #################################################################################
        """Criação da matriz de rigidez global"""
        self.MatrizRigidezGlobal = zeros((self.estrutura.Deslocabilidades*self.estrutura.NumeroDeNos,
                                          self.estrutura.Deslocabilidades*self.estrutura.NumeroDeNos))

        for i in range(1, self.estrutura.NumeroDeBarras+1):

            MatrizIndex = dot(self.estrutura.matriz_rotacao(i).T, dot(self.estrutura.matriz_rigidez_local(i),
                                                                      self.estrutura.matriz_rotacao(i)))

            VetorCorrespondenciaIndex = self.estrutura.vetor_correspondencia(i)

            for j in range(1, 2*self.estrutura.Deslocabilidades+1):
                for jk in range(1, 2*self.estrutura.Deslocabilidades+1):
                    self.MatrizRigidezGlobal[int((VetorCorrespondenciaIndex[j-1, 0])-1),
                                        int((VetorCorrespondenciaIndex[jk-1, 0])-1)] += MatrizIndex[j-1, jk-1]

        self.MatrizRigidezNumeroGrande = zeros((self.estrutura.Deslocabilidades*self.estrutura.NumeroDeNos,
                                           self.estrutura.Deslocabilidades*self.estrutura.NumeroDeNos))
        for i in range(1, (self.estrutura.Deslocabilidades * self.estrutura.NumeroDeNos)+1):
            for j in range(1, (self.estrutura.Deslocabilidades * self.estrutura.NumeroDeNos)+1):
                self.MatrizRigidezNumeroGrande[i-1, j-1] = self.MatrizRigidezGlobal[i-1, j-1]

        for i in range(1, self.estrutura.NumeroDeNos+1):
            for j in range(1, self.estrutura.Deslocabilidades+1):
                if self.estrutura.CondicoesDeContorno[i-1, j-1] == 1:
                    self.MatrizRigidezNumeroGrande[self.estrutura.Deslocabilidades*(i-1)+j-1,
                                              self.estrutura.Deslocabilidades*(i-1)+j-1] = \
                        self.MatrizRigidezNumeroGrande[self.estrutura.Deslocabilidades*(i-1)+j-1,
                                                  self.estrutura.Deslocabilidades*(i-1)+j-1] + self.estrutura.NumeroGrande

        #################################################################################
        """Cálculo dos deslocamentos"""

        Deslocamentos = dot(inv(self.MatrizRigidezNumeroGrande), self.ForcasNodaisNumeroGrande)
        return Deslocamentos

    def reacoes_apoio(self):
        Deslocamentos = self.linear_elastica()
        rr = zeros(((self.estrutura.Deslocabilidades * self.estrutura.NumeroDeNos), 1))
        for i in range(1,( self.estrutura.Deslocabilidades * self.estrutura.NumeroDeNos)+1):
            for j in range(1, (self.estrutura.Deslocabilidades * self.estrutura.NumeroDeNos)+1):
                rr[i-1, 0] = rr[i-1, 0] + self.MatrizRigidezGlobal[i-1,  j-1] * Deslocamentos[j-1, 0]

        ReacoesDeApoio = zeros((self.estrutura.NumeroDeNos, self.estrutura.Deslocabilidades))
        for i in range(1,self.estrutura.NumeroDeNos+1):
            for j in range(1,self.estrutura.Deslocabilidades+1):
                if (self.estrutura.CondicoesDeContorno[i - 1, j-1]) == 1:
                    ReacoesDeApoio[i-1, j-1] = rr[(self.estrutura.Deslocabilidades * (i - 1) + j)-1, 0] -\
                                               self.ForcasNodaisEquivalentes[(self.estrutura.Deslocabilidades * (i - 1)
                                                                              + j) - 1, 0]
                    ReacoesDeApoio[i - 1, j - 1] -= self.estrutura.ForcasNodais[i - 1, j-1]
                else:
                    ReacoesDeApoio[i - 1, j-1] = 0
        print("rr {}".format(rr))
        return ReacoesDeApoio

    def eforcos_solicitantes(self):
        self.linear_elastica()
        uG = zeros((2*self.estrutura.Deslocabilidades, 1))
        EsforcosInternos = zeros((self.estrutura.NumeroDeBarras, 2 * self.estrutura.Deslocabilidades))
        for i in range(1, self.estrutura.NumeroDeBarras+1):
            qi = self.estrutura.vetor_correspondencia(i)
            print(qi)
            for j in range((2 * self.estrutura.Deslocabilidades)):
                uG[j, 0] = self.linear_elastica()[(int(qi[j, 0]))-1, 0]

            uL = dot(self.estrutura.matriz_rotacao(i), uG)
            aLF = (dot(self.estrutura.matriz_rigidez_local(i), uL)) + self.estrutura.engastamento_perfeito(i)
            aGF = dot(self.estrutura.matriz_rotacao(i).T, aLF)
            for j in range((2 * self.estrutura.Deslocabilidades)):
                EsforcosInternos[i-1, j] = aGF[j, 0]

        return EsforcosInternos


#
# R = Analise(Grelha( MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais,
#                 CondicoesDeContorno, G, E, J, I))
# R.linear_elastica()
#
#
# print(R.reacoes_apoio())
