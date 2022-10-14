<img alt="GrelhaPy" src="data/assets/Logo.png" height=120>
<h1 class="anchor">GrelhaPy</h1>
<p>Programa baseado em python com objetivo de realizar a análise estrutural de grelhas.</p>
<ul>
  <li>Fornece os deslocamentos nodais, as reações de apoio, os esforços solicitantes internos nos nós e a matrix de rigidez geral da estrutura</li>
  <li>Baseado na implementação da forma matricial do método dos deslocamentos proposta por <b>Humberto Lima Soriano</b>;</li>
  <li>Interface gráfica que permite a inserção de dados da estrutura em formato de planilhas;</li>
  <li>Tentativa de compartimentação do código de forma a facilitar a implementação futura de outros gêneros de estruturas e outros tipos de análise. </li>
</ul>

<h2>Calculando Jogo rápido</h2>

<p>A inserção da estrutura pode ocorrer insserindo os dados do zero através da interface gráfica, ou carregando um arquivo de excel, em formato padrão, contendo os dados da estrutura.</p>
<p>após o carregamento executado, há necessidade de executar a análise através da guia "Análise" no botão "Executar análise".</p>
<p>* É preciso estar atento ao fato de todos as tabelas estarem preenchidas para a execução da análise.</p>

<h2>Como funciona?</h2>

<p>O programa é composto dos scripts relativos às funcionalidades da interface gráfica e os scripts da implementação do método dos deslocamentos em si.</p>
<p>A parte da análise é basicamente composta de um script que integra a transposição da formulação matricial do método dos deslocamentos para linguagem Python e outro que contém  
  as características particulares da estrutura que se está trabalhando. Desse modo, pretende-se facilitar a inserção de outras estruturas e a modificação do método de análise.<p>


<h2>Licença</h2>
Possivelmente GPL, porém ainda irei atualizar. 

<h2>Contato</h2>
<p>Ficarei feliz em ajudar com suas dúvidas!</p>
<a href="mailto:eng.brunomuniz@outlook.com">eng.brunomuniz@outlook.com</a>
