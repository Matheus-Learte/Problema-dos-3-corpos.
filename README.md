# Simulação de Gravidade com Pyglet
 Esse programa utiliza a biblioteca Pyglet para realizar simulações de sistemas gravitacionais em 2D. Nele se é possível criar n corpos no espaço e definir suas velocidades e direções iniciais. Após isso, a simulação está pronta para ser iniciada, será possível observar a interação que os planetas tem entre si e também um gráfico que contem a decomposição do vetor velocidade (em x e y) ao longo da trajetória em tempo real.

 As imagens de astros disponíveis são apenas Sol, Terra e Lua, cada um com sua massa e tamanho aparente distintos (fora de escala para melhor vizualização)
 
 # Como usar o Simulador
 O simulador não lida bem com colisões, tente evitá-las
 1. Adicionar corpos:
   - Clique na tela para adicionar um corpo.
   - Ainda segurando o botão esquerdo araste o mouse para definir a direção e a velocidade inicial do corpo.
   - Após isso, é possível trocar o astro que está sendo adicionado clicando nos botões 1, 2 e 3, sendo referentes a Lua, Terra e Sol respectivamente
2. Iniciar a simulção:
  - Após ja ter adicionado um corpo com sua direção e velocidade basta apenas apertar Enter e observar a simulação.

# Física implementada
 A física por trás da simulação é relacionada com a Lei da Gravitação Universal prosposta por Isaac Newton, onde a aceleração de cada corpo é calculada considerando as forças gravitacionais que ele sente devido a presença dos outros corpos no sistema.
 
 A Lei proposta por Newton diz que a força gravitacional entre dois corpos é dada por:
 <div align="center">
  <img src="https://latex.codecogs.com/png.latex?\pagecolor{black}\vec{F}%20%3D%20G%20\frac{m_1m_2}{r^2}\hat{r}%20"
alt="Equação da Gravidade" width="200"/>
</div>

onde:

G: Constante gravitacional.

m1 e m2: Massa dos corpos.

r: distância entre os dois corpos.

r(com chapeu em cima): vetor unitário na direção que conecta os dois corpos.

## Leis de Kepler
 A melhor forma de demonstrar as leis do movimento planetário, desenvolvidas por Kepler, é por meio de um sistema de dois corpos em que um está praticamente parado. Por familiaridade trataremos eles como um simples sistema Sol-Terra.

 Resumindo as Leis e relacionando com a simulação:

 1. Lei das óbitas elipticas: A órbita da Terra descreve uma trajetória elíptica, em que o Sol é um de seus centros. No programa, a trajetória do corpo em órbita será demarcada com um traço cheio para melhor vizualização em contraste com o fundo escolhido.
 2. Lei das áreas: Uma linha que une o planeta e o Sol varre áreas iguais durante intervalos de tempo iguais. Simulando o sistema é possível perceber que a Terra é mais veloz quando passa perto do sol ao comparar de quando está longe, isso aliado com o movimento de elipse permite a ocorrencia da segunda lei.
3. A razão entre o quadrado do período orbital de um objeto e o cubo do semi-eixo maior de sua órbita é a mesma para todos os objetos que orbitam o mesmo primário. Como vai simular isso???????????????????????????????
 
## Sistema de Três Corpos
O programa permite que o usuário escolha quaisquer configurações iniciais para os objetos, porém, é interessante deixar algumas situações já pré-preparadas, algumas delas serão soluções estáveis e outra um sistema Lua-Terra-Sol
