grafo = {}
entregas = {}

def ler_arquivo(arquivo):#O(n2)
    vetor_ler = []
    
    try:
        #arquivo_destino = open('entrada-trabalho - complexa.csv', 'r')
        #abre o arquivo informado pelo usuário
        arquivo_destino = open(arquivo, 'r')
        #para cada linha do arquivo 
        for linha in arquivo_destino: #O(n)
            #lê linha por linha e adiciona no vetor_ler, o strip exclui espaços vazios no ínicio e no fim de uma string
            vetor_ler.append(linha.strip())

        arquivo_destino.close()

        vetor_ler = limpar_formatacao_arquivo_lido(vetor_ler) #O(n)
        grafo, entregas = montar_grafo_do_arquivo(vetor_ler)
    
    except ValueError:
        print("valor numérico inválido")
    except IndexError:
        print("matriz do arquivo não está no tamanho correto")
    except FileNotFoundError:
        print("Não encontrado arquivo especificado")
        
    return grafo,entregas

#formatar pra retirar caracteres indevidos
def limpar_formatacao_arquivo_lido(vetor_ler): 
    for i in range(len(vetor_ler)):
        vetor_ler[i] = vetor_ler[i].replace("'", "").replace("‘", "").replace("’", "") #O(1)
    return vetor_ler
    
def montar_grafo_do_arquivo(vetor_ler):
    
    #retorna o n_verticies,n_entregas, pesos e verticies atraves da funcao separar dados do arquivo lido
    n_vertices,n_entregas,pesos,vertices = separar_dados_do_arquivo_lido(vetor_ler) #O(n) + O(n2)
    
    adjacentes = {}
    pesos_temp = {}
    
    #print(pesos)
    #print(vertices)
    #vai de 0 a 4 que é numero de vertices
    for i in range(n_vertices): #O(n2)
        #vai de 0 a 4 que é numero de vertices
        for j in range(n_vertices):
            #se o peso que está na posicao 0 e 0 por exemplo (que é a primeira posição) for maior que 0
            if int(pesos[i][j]) > 0:
                #inicializa com 0
                adjacentes[vertices[j]] = 0
                #associa o adjacente na posicao do vertice em j, o conteudo do peso na posicao i(x) e j(y)
                adjacentes[vertices[j]] += int(pesos[i][j])
                #pesos_temp.append(pesos[i][j])
        grafo[vertices[i]] = adjacentes
        adjacentes = {}
        pesos_temp = {}
    #print(grafo)
    return grafo,entregas

def separar_dados_do_arquivo_lido(vetor_ler): #O(n)
    # cria vetores para pesos,vertices e para ler as entregas
    pesos = []
    vertices = []
    ler_entregas = []

    #numero de vertices está na posição 0 do vetor, ou seja, 4
    n_vertices = int(vetor_ler[0])
    #numero de entregas está na posição 6 do vetor, ou seja, 3
    n_entregas = int(vetor_ler[n_vertices + 2])

    for i in range(2, n_vertices + 2):
        #adiciona ao vetor pesos, os pesos entre as posições 2 e 6 da matriz
        pesos.append(vetor_ler[i].split(','))

    for i in range(0, n_entregas):
        #adiciona ao vetor ler_entregas, ou seja, as entregas entre a posição 7 a 9 
        ler_entregas.append(vetor_ler[n_vertices + 3 + i].split(','))

    for i in range(n_entregas):
        #associa a entrega na posição i(x) que vai de 0 a 3 e na posição 1(y), recebe o conteudo do vetor ler_entregas na posição i(x) e na posicao 0(y), 
        #e recebe o conteudo do vetor ler_arquivo na posição i(x) e 2(y)
        entregas[ler_entregas[i][1]] = [ler_entregas[i][0], ler_entregas[i][2]]

    #vetor vertices adiciona o conteudo do vetor_ler na posicao 1, usando o separador virgula
    vertices.append(vetor_ler[1].split(','))
    vertices = vertices[0]

    return n_vertices,n_entregas,pesos,vertices