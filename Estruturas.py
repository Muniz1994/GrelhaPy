from numpy import array, zeros, absolute


class Grelha:

    def __init__(self, MatrizDeCoordenadas, MatrizDeConectividade, ForcasDistribuidas, ForcasNodais,
                CondicoesDeContorno, G, E, J, I):

        self.MatrizDeCoordenadas = MatrizDeCoordenadas
        self.MatrizDeConectividade = MatrizDeConectividade
        self.NumeroDeNos = self.MatrizDeCoordenadas.shape[0]
        self.NumeroDeBarras = self.MatrizDeConectividade.shape[0]
        self.ForcasDistribuidas = ForcasDistribuidas
        self.ForcasNodais = ForcasNodais
        self.CondicoesDeContorno = CondicoesDeContorno
        self.G = G
        self.E = E
        self.J = J
        self.I = I

        self.DeslocamentosPrescritos = zeros((self.NumeroDeNos, 3))

        self.Deslocabilidades = 3

        self.NumeroGrande = 1E15

    def comprimento_barra(self, i):

        return int((((self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 1])-1, 0] -
                      self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 0])-1, 0])**2) +
                    ((self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 1])-1, 1] -
                      self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 0])-1, 1])**2))**0.5)

    def matriz_rigidez_local(self, i):

        x = array(([((self.G[i-1, 0]*self.J[i-1, 0]) / self.comprimento_barra(i)), 0, 0,
                       ((-self.G[i - 1, 0] * self.J[i - 1, 0]) / self.comprimento_barra(i)), 0, 0],
                      # segunda linha
                      [0, ((4*self.E[i-1, 0]*self.I[i-1, 0]) / self.comprimento_barra(i)),
                       ((-6 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 2), 0,
                       ((2 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i)),
                       ((6 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 2)],
                      # Terceira linha
                      [0, ((-6*self.E[i-1, 0]*self.I[i-1, 0]) / self.comprimento_barra(i) ** 2),
                       ((12 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 3), 0,
                       ((-6 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 2),
                       ((-12 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 3)],
                      # Quarta Linha
                      [((-self.G[i-1, 0]*self.J[i-1, 0]) / self.comprimento_barra(i)), 0, 0,
                       ((self.G[i - 1, 0] * self.J[i - 1, 0]) / self.comprimento_barra(i)), 0, 0],
                      # Quinta linha
                      [0, ((2*self.E[i-1, 0]*self.I[i-1, 0]) / self.comprimento_barra(i)),
                       ((-6 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 2), 0,
                       ((4 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i)),
                       ((6 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 2)],
                      # Sexta linha
                      [0, ((6*self.E[i-1, 0]*self.I[i-1, 0]) / self.comprimento_barra(i) ** 2),
                       ((-12 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 3), 0,
                       ((6 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 2),
                       ((12 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 3)]))
        return x

    def engastamento_perfeito(self, i):

        engperf = zeros((6, 1))
        engperf[0, 0] = 0
        engperf[3, 0] = 0
        engperf[2, 0] = -(self.ForcasDistribuidas[i-1, 0] * self.comprimento_barra(i)) / 2
        engperf[5, 0] = engperf[2, 0]
        engperf[1, 0] = (self.ForcasDistribuidas[i-1, 0] * (self.comprimento_barra(i) ** 2) / 12)
        engperf[4, 0] = - engperf[1, 0]
        return engperf

    def matriz_rotacao(self, i):

        x = zeros((2*self.Deslocabilidades, 2*self.Deslocabilidades))
        x[0, 0] = absolute(((self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 1])-1, 0]
                                - self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 0])-1, 0]) / self.comprimento_barra(i)))
        x[0, 1] = absolute(((self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 1])-1, 1]
                                - self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 0])-1, 1]) / self.comprimento_barra(i)))
        x[1, 0] = - x[0, 1]
        x[1, 1] = x[0, 0]
        x[2, 2] = 1

        for ii in range(1, self.Deslocabilidades+1):
            for ij in range(1, self.Deslocabilidades+1):
                x[2+ii, 2+ij] = x[ii-1, ij-1]
        return x

    def vetor_correspondencia(self, i):

        x = zeros((2*self.Deslocabilidades, 1))

        if self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 1])-1, 0] >= \
                self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 0]) - 1, 0] and \
                self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 1])-1, 1] >= \
                self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 0])-1, 1]:

            y = 0

            for j in range(1, 3):

                for jk in range(1, self.Deslocabilidades+1):

                    y += 1

                    w = self.Deslocabilidades * (self.MatrizDeConectividade[i-1, j-1] - 1) + jk

                    x[y-1, 0] = int(w)

        else:

            y = 3

            j = 1

            for jk in range(1,self.Deslocabilidades+1):

                y += 1

                w = self.Deslocabilidades * (self.MatrizDeConectividade[i-1, j-1] - 1) + jk

                x[y-1, 0] = int(w)

            y = 0

            j = 2

            for jk in range(1, self.Deslocabilidades+1):

                y += 1

                w = self.Deslocabilidades * (self.MatrizDeConectividade[i-1, j-1] - 1) + jk

                x[y-1, 0] = int(w)
        return x

class ElementoIsolado:

    def __init__(self, Deslocamento,Reacoes_apoio, ESI, comprimento):

        self.MatrizDeCoordenadas = None
        self.MatrizDeConectividade = None
        self.NumeroDeNos = int(comprimento)
        self.NumeroDeBarras = self.NumeroDeNos -1
        self.ForcasDistribuidas = ForcasDistribuidas
        self.ForcasNodais = ForcasNodais
        self.CondicoesDeContorno = CondicoesDeContorno
        self.G = G
        self.E = E
        self.J = J
        self.I = I

        self.DeslocamentosPrescritos = zeros((self.NumeroDeNos, 3))

        self.Deslocabilidades = 3

        self.NumeroGrande = 1E15

    def matriz_de_conectividade(self):
        matriz = zeros((self.NumeroDeBarras))
        for i in range(1,self.NumeroDeBarras+1):
                matriz[i, 0] = i
                matriz[i, 1] = i+1

    def matriz_de_coordenadas(self):
        matriz = zeros((self.NumeroDeNos))
        for i in range(self.NumeroDeNos):
                matriz[i, 0] = i
                matriz[i, 1] = 0

    def comprimento_barra(self, i):

        return int((((self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 1])-1, 0] -
                      self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 0])-1, 0])**2) +
                    ((self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 1])-1, 1] -
                      self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 0])-1, 1])**2))**0.5)

    def matriz_rigidez_local(self, i):

        x = array(([((self.G[i-1, 0]*self.J[i-1, 0]) / self.comprimento_barra(i)), 0, 0,
                       ((-self.G[i - 1, 0] * self.J[i - 1, 0]) / self.comprimento_barra(i)), 0, 0],
                      # segunda linha
                      [0, ((4*self.E[i-1, 0]*self.I[i-1, 0]) / self.comprimento_barra(i)),
                       ((-6 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 2), 0,
                       ((2 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i)),
                       ((6 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 2)],
                      # Terceira linha
                      [0, ((-6*self.E[i-1, 0]*self.I[i-1, 0]) / self.comprimento_barra(i) ** 2),
                       ((12 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 3), 0,
                       ((-6 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 2),
                       ((-12 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 3)],
                      # Quarta Linha
                      [((-self.G[i-1, 0]*self.J[i-1, 0]) / self.comprimento_barra(i)), 0, 0,
                       ((self.G[i - 1, 0] * self.J[i - 1, 0]) / self.comprimento_barra(i)), 0, 0],
                      # Quinta linha
                      [0, ((2*self.E[i-1, 0]*self.I[i-1, 0]) / self.comprimento_barra(i)),
                       ((-6 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 2), 0,
                       ((4 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i)),
                       ((6 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 2)],
                      # Sexta linha
                      [0, ((6*self.E[i-1, 0]*self.I[i-1, 0]) / self.comprimento_barra(i) ** 2),
                       ((-12 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 3), 0,
                       ((6 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 2),
                       ((12 * self.E[i - 1, 0] * self.I[i - 1, 0]) / self.comprimento_barra(i) ** 3)]))
        return x

    def engastamento_perfeito(self, i):

        engperf = zeros((6, 1))
        engperf[0, 0] = 0
        engperf[3, 0] = 0
        engperf[2, 0] = -(self.ForcasDistribuidas[i-1, 0] * self.comprimento_barra(i)) / 2
        engperf[5, 0] = engperf[2, 0]
        engperf[1, 0] = (self.ForcasDistribuidas[i-1, 0] * (self.comprimento_barra(i) ** 2) / 12)
        engperf[4, 0] = - engperf[1, 0]
        return engperf

    def matriz_rotacao(self, i):

        x = zeros((2*self.Deslocabilidades, 2*self.Deslocabilidades))
        x[0, 0] = absolute(((self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 1])-1, 0]
                                - self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 0])-1, 0]) / self.comprimento_barra(i)))
        x[0, 1] = absolute(((self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 1])-1, 1]
                                - self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 0])-1, 1]) / self.comprimento_barra(i)))
        x[1, 0] = - x[0, 1]
        x[1, 1] = x[0, 0]
        x[2, 2] = 1

        for ii in range(1, self.Deslocabilidades+1):
            for ij in range(1, self.Deslocabilidades+1):
                x[2+ii, 2+ij] = x[ii-1, ij-1]
        return x

    def vetor_correspondencia(self, i):

        x = zeros((2*self.Deslocabilidades, 1))

        if self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 1])-1, 0] >= \
                self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 0]) - 1, 0] and \
                self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 1])-1, 1] >= \
                self.MatrizDeCoordenadas[int(self.MatrizDeConectividade[i-1, 0])-1, 1]:

            y = 0

            for j in range(1, 3):

                for jk in range(1, self.Deslocabilidades+1):

                    y += 1

                    w = self.Deslocabilidades * (self.MatrizDeConectividade[i-1, j-1] - 1) + jk

                    x[y-1, 0] = int(w)

        else:

            y = 3

            j = 1

            for jk in range(1,self.Deslocabilidades+1):

                y += 1

                w = self.Deslocabilidades * (self.MatrizDeConectividade[i-1, j-1] - 1) + jk

                x[y-1, 0] = int(w)

            y = 0

            j = 2

            for jk in range(1, self.Deslocabilidades+1):

                y += 1

                w = self.Deslocabilidades * (self.MatrizDeConectividade[i-1, j-1] - 1) + jk

                x[y-1, 0] = int(w)
        return x
