from numpy import array, dot, zeros

from numpy.linalg import inv

from copy import copy

from Grelhapy.Estruturas import Grelha

# Variável a ser modificada


# MatrizDeCoordenadas = array(([0, 0], [0, 4], [6, 4]))
# MatrizDeConectividade = array(([1, 2], [2, 3]))
# ForcasDistribuidas = array(([-10], [-5]))
# ForcasNodais = array(([0, 0, 0], [0, 0, -5], [0, 0, 0]))
# CondicoesDeContorno = array(([1, 1, 1], [0, 0, 0], [1, 1, 1]))
# G = array(([103.56491E8], [103.56491E8]))
# E = array(([248.55578E8], [248.55578E8]))
# J = array(([4.086E-10], [4.086E-10]))
# I = array(([2.043E-10], [2.043E-10]))


# Vetor de forças nodais equivalentes
class Analise:

    def __init__(self, Estrutura):

        self.estrutura = Estrutura
        self.MatrizRigidezGlobal = None

    def linear_elastica(self):
        self.ForcasNodaisEquivalentes = zeros((self.estrutura.Deslocabilidades * self.estrutura.NumeroDeNos, 1))

        for i in range(1, self.estrutura.NumeroDeBarras+1):

            EngastamentoPerfeitoGlobal = dot(self.estrutura.matriz_rotacao(i).T, self.estrutura.engastamento_perfeito(i))

            VetorCorrespondenciaIndex = self.estrutura.vetor_correspondencia(i)

            for j in range(1, (2*self.estrutura.Deslocabilidades)+1):

                self.ForcasNodaisEquivalentes[int((VetorCorrespondenciaIndex[j-1, 0])-1), 0] -= EngastamentoPerfeitoGlobal[j-1, 0]

        ForcasNodaisCombinadas = copy(self.ForcasNodaisEquivalentes)

        for i in range(1, self.estrutura.NumeroDeNos+1):

            for j in range(1, self.estrutura.Deslocabilidades+1):

                ForcasNodaisCombinadas[(((i-1)*self.estrutura.Deslocabilidades) + j)-1, 0] += self.estrutura.ForcasNodais[i-1, j-1]

        self.MatrizRigidezGlobal = zeros((self.estrutura.Deslocabilidades*self.estrutura.NumeroDeNos, self.estrutura.Deslocabilidades*self.estrutura.NumeroDeNos))

        for i in range(1, self.estrutura.NumeroDeBarras+1):

            MatrizIndex = dot(self.estrutura.matriz_rotacao(i).T, dot(self.estrutura.matriz_rigidez_local(i), self.estrutura.matriz_rotacao(i)))

            VetorCorrespondenciaIndex = self.estrutura.vetor_correspondencia(i)

            for j in range(1, 2*self.estrutura.Deslocabilidades+1):
                for jk in range(1, 2*self.estrutura.Deslocabilidades+1):
                    self.MatrizRigidezGlobal[int((VetorCorrespondenciaIndex[j-1, 0])-1),
                                        int((VetorCorrespondenciaIndex[jk-1, 0])-1)] += MatrizIndex[j-1, jk-1]

        MatrizRigidezNumeroGrande = zeros((self.estrutura.Deslocabilidades*self.estrutura.NumeroDeNos, self.estrutura.Deslocabilidades*self.estrutura.NumeroDeNos))
        for i in range(1, (self.estrutura.Deslocabilidades * self.estrutura.NumeroDeNos)+1):
            for j in range(1, (self.estrutura.Deslocabilidades * self.estrutura.NumeroDeNos)+1):
                MatrizRigidezNumeroGrande[i-1, j-1] = self.MatrizRigidezGlobal[i-1, j-1]

        for i in range(1, self.estrutura.NumeroDeNos+1):
            for j in range(1, self.estrutura.Deslocabilidades+1):
                if self.estrutura.CondicoesDeContorno[i-1, j-1] == 1:
                    MatrizRigidezNumeroGrande[self.estrutura.Deslocabilidades*(i-1)+j-1, self.estrutura.Deslocabilidades*(i-1)+j-1] = \
                        MatrizRigidezNumeroGrande[self.estrutura.Deslocabilidades*(i-1)+j-1, self.estrutura.Deslocabilidades*(i-1)+j-1] + self.estrutura.NumeroGrande

        ForcasNodaisNumeroGrande = zeros((self.estrutura.Deslocabilidades*self.estrutura.NumeroDeNos, 1))
        for i in range(1, self.estrutura.NumeroDeNos+1):
            for j in range(1, self.estrutura.Deslocabilidades+1):
                if self.estrutura.CondicoesDeContorno[i-1, j-1] == 1:
                    ForcasNodaisNumeroGrande[(self.estrutura.Deslocabilidades*(i-1)+j)-1, 0] = \
                        ForcasNodaisCombinadas[(self.estrutura.Deslocabilidades*(i-1)+j)-1, 0] + \
                        self.estrutura.NumeroGrande * self.estrutura.DeslocamentosPrescritos[i-1, j-1]
                else:
                    ForcasNodaisNumeroGrande[(self.estrutura.Deslocabilidades*(i-1)+j)-1, 0] =\
                        ForcasNodaisCombinadas[(self.estrutura.Deslocabilidades*(i-1)+j)-1, 0]

        Deslocamentos = dot(inv(MatrizRigidezNumeroGrande), ForcasNodaisNumeroGrande)
        return Deslocamentos

    def reacoes_apoio(self):
        self.linear_elastica()
        rr = zeros(((self.estrutura.Deslocabilidades* self.estrutura.NumeroDeNos), 1))
        for i in range((self.estrutura.Deslocabilidades * self.estrutura.NumeroDeNos)+1):
            for j in range((self.estrutura.Deslocabilidades * self.estrutura.NumeroDeNos)+1):
                rr[i-1, 0] = rr[i-1, 0] + self.MatrizRigidezGlobal[i-1,  j-1] * self.linear_elastica()[j-1, 0]

        ReacoesDeApoio = zeros((self.estrutura.NumeroDeNos, self.estrutura.Deslocabilidades))
        for i in range(self.estrutura.NumeroDeNos+1):
            for j in range(self.estrutura.Deslocabilidades+1):
                if (self.estrutura.CondicoesDeContorno[i - 1, j-1]) == 1:
                    ReacoesDeApoio[i-1, j-1] = rr[(self.estrutura.Deslocabilidades * (i - 1) + j)-1, 0] - self.ForcasNodaisEquivalentes[(self.estrutura.Deslocabilidades * (i - 1) + j) -1, 0]
                    ReacoesDeApoio[i - 1, j - 1] -= self.estrutura.ForcasNodais[i - 1, j-1]
                else:
                    ReacoesDeApoio[i - 1, j-1] = 0
        return ReacoesDeApoio

    def eforcos_solicitantes(self):
        self.linear_elastica()
        uG = zeros((2*self.estrutura.Deslocabilidades, 1))
        EsforcosInternos = zeros((self.estrutura.NumeroDeBarras, 2 * self.estrutura.Deslocabilidades))
        for i in range(1, self.estrutura.NumeroDeBarras+1):
            qi = self.estrutura.vetor_correspondencia(i)
            for j in range((2 * self.estrutura.Deslocabilidades)):
                uG[j, 0] = self.linear_elastica()[(int(qi[j, 0]))-1, 0]

            uL = dot(self.estrutura.matriz_rotacao(i), uG)
            aLF = (dot(self.estrutura.matriz_rigidez_local(i), uL)) + self.estrutura.engastamento_perfeito(i)
            for j in range((2 * self.estrutura.Deslocabilidades)):
                EsforcosInternos[i-1, j] = aLF[j, 0]

        return EsforcosInternos

#
# R = Analise(Grelha( MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais,
#                 CondicoesDeContorno, G, E, J, I))
# R.linear_elastica()
#
# print(R.reacoes_apoio())