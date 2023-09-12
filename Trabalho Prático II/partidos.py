import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def obter_filtro_usuario():
    ano = input("Digite o ano que deseja visualizar os dados: ")

    escolha_partidos = input("Deseja buscar partidos específicos (1) ou todos (2)? ")

    if escolha_partidos == "1":
        num_partidos = int(input("Quantos partidos deseja buscar? "))
        partidos_selecionados = []
        for i in range(num_partidos):
            partido = input(f"Digite o nome do partido {i+1}: ")
            partidos_selecionados.append(partido)
        
        threshold = input("Qual o Threshold deseja considerar? ")  
        return ano, partidos_selecionados, threshold
    
    elif escolha_partidos == "2":
        todos_partidos = "datasets/politicians" + ano + ".txt"
        partidos_sem_duplicata = obter_partidos_do_arquivo(todos_partidos)
        print(partidos_sem_duplicata)
        threshold = input("Qual o Threshold deseja considerar? ")  
        return ano, partidos_sem_duplicata, threshold  # Retorna o vetor vazio
    else:
        print("Opção inválida.")
        return None, None, None

def obter_partidos_do_arquivo(nome_arquivo):
    partidos_sem_duplicata = set()  
    
    with open(nome_arquivo, 'r', encoding='utf-8-sig') as file:
        for linha in file:
            elementos = linha.strip().split(';')
            if len(elementos) >= 2:
                partidos_sem_duplicata.add(elementos[1])  
    
    return list(partidos_sem_duplicata)

# def partidos_definidos(selecionados, partidos, ano, threshold):
#     obter_partidos = [partido for i, partido in enumerate(partidos) if selecionados[i].get()]
#     funcao_normalizacao(obter_partidos, ano, threshold)


def funcao_normalizacao(partidos_obtidos, ano, treshold):
    
    arqDeputados = "datasets/politicians" + ano + ".txt"
    arqGrafo = "datasets/graph" + ano + ".txt"

    thresholdGrafo = nx.Graph()
    grafo = nx.Graph()
    partidoDoDeputado = {}

    with open(arqDeputados, 'r', encoding='utf-8') as file:
        deputados = []
        quantidadeVotos = {}
        linha = file.readline().strip()
        while linha:
            opcoes = linha.split(';')
            if opcoes[1] in partidos_obtidos:
                deputados.append(opcoes[0])
                partidoDoDeputado[opcoes[0]] = opcoes[1]
                quantidadeVotos[opcoes[0]] = int(opcoes[2])
            linha = file.readline().strip()

    with open(arqGrafo, 'r', encoding='utf-8') as file:
        linha = file.readline().strip()
        while linha:
            opcoes = linha.split(';')
            if opcoes[0] in deputados and opcoes[1] in deputados:
                peso = int(opcoes[2]) / min(quantidadeVotos[opcoes[0]], quantidadeVotos[opcoes[1]])
                grafo.add_edge(opcoes[0], opcoes[1], weight=peso)
                thresholdGrafo.add_edge(opcoes[0], opcoes[1], weight=1 - peso)
                if peso < float(treshold):
                    thresholdGrafo.remove_edge(opcoes[0], opcoes[1])
            linha = file.readline().strip()

    imagens(thresholdGrafo, partidos_obtidos, partidoDoDeputado, grafo)

def criacao_grafico(betweenness):
    fig, center = plt.subplots(figsize=(15, 8))

    betweenness_sorted = dict(sorted(betweenness.items(), key=lambda item: item[1], reverse=True))

    bar_labels = list(betweenness_sorted.keys())  
    bar_heights = list(betweenness_sorted.values()) 
    bar_colors = 'tab:green'

    center.bar(bar_labels, bar_heights, color=bar_colors)

    center.set_ylabel('Betweenness')
    center.set_xlabel('Deputados')
    center.set_title('Centralidade')

    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.tight_layout()

    plt.savefig("representacao_grafico.png", dpi=140, bbox_inches='tight')
    plt.show()

def plotagem_grafico(grafo, partidos, partidoDoDeputado):
    colorsDoPartido = {}
    colorDoNo = []

    colors = [
        (0.0, 0.0, 1.0),
        (1.0, 0.0, 0.0), 
        (0.0, 1.0, 0.0), 
        (1.0, 1.0, 0.0), 
        (0.0, 1.0, 1.0), 
        (1.0, 0.0, 1.0),
        (0.5019607843137255, 0.0, 0.0),   
        (0.0, 0.5019607843137255, 0.0),  
        (0.0, 0.0, 0.5019607843137255),   
        (0.5019607843137255, 0.5019607843137255, 0.0),   
        (0.5019607843137255, 0.0, 0.5019607843137255),   
        (0.0, 0.5019607843137255, 0.5019607843137255),   
        (0.7529411764705882, 0.7529411764705882, 0.7529411764705882), 
        (0.5019607843137255, 0.5019607843137255, 0.5019607843137255),
        (1.0, 0.6470588235294118, 0.0),   
        (1.0, 0.7529411764705882, 0.796078431372549), 
        (1.0, 0.8941176470588236, 0.7098039215686275), 
        (0.0, 0.0, 0.0),      
        (1.0, 1.0, 1.0), 
        (0.0, 0.0, 0.27450980392156865)       
    ]

    for i in range(len(partidos)):
        colorsDoPartido[partidos[i]] = colors[i]
    
    for deputado in grafo.nodes():
        colorDoNo.append(colorsDoPartido[partidoDoDeputado[deputado]])
    
    layout = nx.spring_layout(grafo)
    fig, center = plt.subplots()
    plt.figure(num=None, figsize=(12, 8), dpi=140)
    nx.draw(grafo, pos=layout, with_labels=True, node_size=20, node_color=colorDoNo, font_size=7, width=0.1)
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colorsDoPartido[partido], markersize=10, label=partido) for partido in partidos]
    plt.legend(handles=handles, title="Partidos", loc='upper right')
    plt.savefig("representacao_plotagem.png", bbox_inches='tight')
    plt.show()

def criacao_heatmap(grafo, partidoDoDeputado, partidos_obtidos):
    labels = []
    partidoLabels = []

    for i in range(len(partidos_obtidos)):
        for deputado in partidoDoDeputado:
            if partidoDoDeputado[deputado] == partidos_obtidos[i]:
                partidoLabels.append((deputado, partidos_obtidos[i]))

    partidoLabels = sorted(partidoLabels, key=lambda x: x[1])

    matrizAdjacencias = np.zeros((len(partidoLabels), len(partidoLabels)))

    for i, (dep1, partido1) in enumerate(partidoLabels):
        for j, (dep2, partido2) in enumerate(partidoLabels):
            if grafo.has_edge(dep1, dep2):
                matrizAdjacencias[i, j] = grafo[dep1][dep2]['weight']

    for dep, partido in partidoLabels:
        deputado = f"{dep} ({partido})"
        labels.append(deputado)

    fig, center = plt.subplots(figsize=(12, 6), dpi=160)
    plt.xticks(rotation=45, ha='right', fontsize=4)
    plt.yticks(range(len(partidoLabels)), labels, fontsize=4)
    plt.plot(labels, labels)

    heatmap = center.imshow(matrizAdjacencias, cmap='hot', interpolation='nearest', aspect='auto')
    fig.colorbar(heatmap, ax=center)
    
    plt.subplots_adjust(bottom=0.3)
    
    plt.title('Heatmap')
    plt.savefig("representacao_heatmap.png", bbox_inches='tight')
    plt.show()

def imagens(thresholdGrafo, partidos_obtidos, partidoDeputado, grafo):
    betweenness = nx.betweenness_centrality(thresholdGrafo)
    criacao_grafico(betweenness)
    plotagem_grafico(thresholdGrafo, partidos_obtidos, partidoDeputado)
    criacao_heatmap(grafo, partidoDeputado, partidos_obtidos)
