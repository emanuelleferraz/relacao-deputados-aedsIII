from partidos import *

#Interação com o usuário e geração dos gráficos de plotagem, heatmap e betweenness
ano, partidos, threshold = obter_filtro_usuario()
funcao_normalizacao(partidos, ano, threshold)