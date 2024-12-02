# Simulação de Gravidade com Pyglet
 Esse programa utiliza a biblioteca Pyglet para realizar simulações de sistemas gravitacionais em 2D. Nele se é possível criar n corpos no espaço e definir suas velocidades e direções iniciais. Após isso, a simulação está pronta para ser iniciada, será possível observar a interação que os planetas tem entre si e também um gráfico que contem a decomposição do vetor velocidade (em x e y) ao longo da trajetória em tempo real.

 As imagens de astros disponíveis são apenas Sol, Terra e Lua, cada um com sua massa e tamanho aparente distintos (fora de escala para melhor vizualização)
 
 # Como usar o Simulador
 O simulador não lida bem com colisões, tente evitá-las
 1. Adicionar corpos:
   - Clique na tela para adicionar um corpo.
   - Ainda segurando o botão esquerdo araste o mouse para definir a direção e a velocidade inicial do corpo.
   - Por fim, é possível trocar o astro que está sendo adicionado clicando nos botões 1, 2 e 3, sendo referentes a Lua, Terra e Sol respectivamente
2. Iniciar a simulção:
  - Após ja ter adicionado um corpo com sua direção e velocidade basta apenas apertar Enter e observar a simulação.
3. Parar a simulação:
  - Para reiniciar a simulação e iniciar uma nova basta apertar a tecla "R"
  - Para fechar o programa basta que aperte Enter enquanto a simulação esteja rodando.

# Física implementada
 A física por trás da simulação é relacionada com a Lei da Gravitação Universal prosposta por Isaac Newton, onde a aceleração de cada corpo é calculada considerando as forças gravitacionais que ele sente devido a presença dos outros corpos no sistema.
 
 A Lei proposta por Newton diz que a força gravitacional entre dois corpos é dada por:
 
<div align="center">
  <img src="/img/offof(1).png" alt="Formula" width="200">
</div>

onde:

$G$: Constante de gravitação, tem valor de $6,67 \times 10^{-11} N \, m^2 \, kg^{-2}.$

$m_1$ e $m_2$: Massa dos corpos 1 e 2 respectivamente.

$r$: distância entre os dois corpos.

$\hat{r}$: versor radial centrado no corpo que produz a força.

## Leis de Kepler
 A melhor forma de demonstrar as leis do movimento planetário, desenvolvidas por Kepler, é por meio de um sistema de dois corpos em que um está praticamente parado. Por familiaridade trataremos eles como um simples sistema Sol-Terra.

 Resumindo as Leis e relacionando com a simulação:

 1. Lei das óbitas elipticas: A órbita da Terra descreve uma trajetória elíptica, em que o Sol é um de seus centros. No programa, a trajetória do corpo em órbita será demarcada com um traço cheio para melhor vizualização em contraste com o fundo escolhido.
   
 2. Lei das áreas: Uma linha que une o planeta e o Sol varre áreas iguais durante intervalos de tempo iguais. Simulando o sistema é possível perceber que a Terra é mais veloz quando passa perto do sol ao comparar de quando está longe, isso aliado com o movimento de elipse permite a ocorrencia da segunda lei.
 
3. A razão entre o quadrado do período orbital de um objeto e o cubo do semi-eixo maior de sua órbita é a mesma para todos os objetos que orbitam o mesmo primário. Como vai simular isso???????????????????????????????
 
## Sistema de Três Corpos
O programa permite que o usuário escolha quaisquer configurações iniciais para os objetos, porém, é interessante deixar algumas situações já pré-preparadas, algumas delas serão soluções estáveis e outra um sistema Lua-Terra-Sol
