
![GrelhaPy Logo](data/assets/Gpyicon.png)

# GrelhaPy

Programa baseado em python com objetivo de realizar a análise estrutural de grelhas.

- Fornece os deslocamentos nodais, as reações de apoio, os esforços solicitantes internos nos nós e a matriz de rigidez geral da estrutura
- Baseado na implementação da forma matricial do método dos deslocamentos proposta por Humberto Lima Soriano;
- Interface gráfica que permite a inserção de dados da estrutura em formato de planilhas;
- Desenvolvido com uma lógica direcionada a objetos e escalável, de forma a facilitar a implementação futura de outros tipos de estruturas e análises. 



## Uso/Exemplos

A execução da análise ocorre a partir do seguinte fluxo:

1. Definição das características geométricas da estrutura (nós e barras) e das condições de restrição dos nós;
2. Definição das características dos materiais da estrutura (módulos de elasticidade);
3. Definição das forças atuantes na estrutura, tanto concentradas como distribuí;
4. Execução da análise;

Antes da execução da análise, o programa irá conferir a consistência dos dados inseridos, informando caso encontre algum problema.


Como resultado da análise, são fornecidos os seguintes dados:

* Deslocamentos nodais;
* Reações de apoio;
* Esforços solicitantes internos nos nós;
* Matriz de rigidez geral da estrutura.

![Matriz de rigidez](data\assets\MatrizRigidez.png)
<p align = "center">
Fig.1 - Interface do programa com apresentação da matriz de rigidêz geral.
</p>

## Licença

[MIT](https://choosealicense.com/licenses/mit/)


## Autores

[@BrunoMuniz](https://github.com/Muniz1994)

