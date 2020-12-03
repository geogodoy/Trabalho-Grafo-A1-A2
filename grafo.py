class Job: 
    def __init__(self, start, finish, profit, path):
        self.start = start 
        self.finish = finish 
        self.profit = profit
        self.path = path

#Algortimo de Dijkstra usado para encontrar o caminho mais curto no grafo
def dijkstra(graph, start, end):
    queue,seen = [(0, start, [])], set()
    while True:
        (cost, v, path) = heapq.heappop(queue)
        if v not in seen:
            path = path + [v]
            seen.add(v)
            if v == end:
                return cost, path
            for (next, c) in graph[v].items():
                heapq.heappush(queue, (cost + c, next, path))

#Método que retorna os caminhos menores
def menores_caminhos(entregas,graph,job):
    #associa o primeiro elemento ao A no caso
    inicio = list(graph.keys())[0];
    
    #para cada destino das entregas
    for destino in entregas:  #complexidade: O(e) * tudo abaixo
        try:
            #através do algoritmo de Dijkstra retorna o tempo e caminho de ida, passando o inicio e o destino
            tempo_ida, caminho_ida = dijkstra(graph,inicio, destino) #complexidade: O((n+m)*logn)

            #através do algoritmo de Dijkstra retorna o tempo e caminho de volta, porém inventendo os parâmetros passando o destino por primeiro e depois o inicio
            tempovolta, caminho_volta = dijkstra(graph,destino, inicio)#complexidade: O(idem)
            #Calcula o tempo final baseado nos tempos de ida e volta dos destinos
            tempofinal = tempo_ida + tempovolta#complexidade:O(1)
            #
            tempoinicial = int(entregas[destino][0])#complexidade:O(1)
            lucroentrega = int(entregas[destino][1])#complexidade:O(1)
            caminho = list([caminho_ida] + [caminho_volta])#complexidade:O(1)
            #armazena todos os caminhos
            job.append(Job(tempoinicial, tempoinicial + tempofinal, lucroentrega, caminho))#complexidade:O(1)
        except:
            print("Não há caminho para a entrega : ",destino,"\n")
    return job


def Encontrar_Predecessor(job,start_index): #complexidade: O(nlogn) ou O(n2)
    escolhido = 0
    for i in reversed(range(0,start_index)):
        if job[i].finish <= job[start_index].start:
            return i
    return escolhido

def schedule(job): 

    job = merge_sort(job) #complexidade: OK O(e log e)
    for j in job: #complexidade: O(e)
        print("Começo :",j.start," Fim :",j.finish," Lucro : ",j.profit)
    pre=0
    n = len(job)
    table_pre = [0 for _ in range(n)] #complexidade: p(J)
    table_lucro = [0 for _ in range(n)] #complexidade: v(J)
    table_max = [0 for _ in range(n)] #complexidade: M[J]

    ### esse eh o wis ###
    for i in range(1,n): #complexidade: O(e)
        table_lucro[i] = job[i].profit
        pre = Encontrar_Predecessor(job,i) #complexidade: O(?)
        if pre != 0:
            table_pre[i] = pre
        table_max[i] = max(table_lucro[i] + table_max[table_pre[i]], table_max[i - 1]) #complexidade: O(1)

    print("Table lucro,Tabela pre, Tabela Max :")
    print(table_lucro)
    print(table_pre)
    print(table_max)
        
    lucro_max=0
    lista_lucro = Find_Solution(n-1,table_pre,table_lucro,table_max,[])
    for indice in lista_lucro:
        lucro_max += int(job[indice].profit)

    return lucro_max,lista_lucro,job

def Find_Solution(j,table_pre,table_lucro,table_max,lista_lucro): #O(e)
    if (j == 0):# or cont >= j):
        print("fim")
        return lista_lucro
    elif ((table_lucro[j] + table_max[table_pre[j]]) > table_max[j-1]):
        #print(j)
        lista_lucro.append(j)
        return Find_Solution(table_pre[j],table_pre,table_lucro,table_max,lista_lucro)
    else: 
        return Find_Solution(j-1,table_pre,table_lucro,table_max,lista_lucro)

########## MERGE SORT ###############

def merge(llist, rlist):
        final = []
        while llist or rlist:
                if len(llist) and len(rlist):
                        if llist[0].finish < rlist[0].finish:
                                final.append(llist.pop(0))
                        else:
                                final.append(rlist.pop(0))
                if not len(llist):
                                if len(rlist): final.append(rlist.pop(0))

                if not len(rlist):
                                if len(llist): final.append(llist.pop(0))

        return final

def merge_sort(list):
        if len(list) < 2: return list
        mid = len(list) // 2
        return merge(merge_sort(list[:mid]), merge_sort(list[mid:]))

if __name__ == "__main__":
    import heapq
    import lerArquivo
    while(1):
        arquivo = ''
        print("Por favor informe o caminho para seu arquivo juntamente com sua extensão. Exemplo: arquivo.csv : ")
        arquivo = input(arquivo)
        print(arquivo)
        try:
            graph,entregas = lerArquivo.ler_arquivo(arquivo) #complexidade: O(n2)
        except:
            print("O arquivo informado não foi possível manipilá-lo")
            continue
        print("Grafo\n", graph)
        print("Lista de Entregas\n", entregas,"\n")
        job = []
        job = menores_caminhos(entregas,graph,job) #complexidade: O(e)*(2*(O((n+m)*logn))
        job.append(Job(0,0,0,[]))
        
        lucro_max, lucro_list, job = schedule(job)

        print("Lista de Entregas realizadas : ", len(lucro_list))
        caminhos_lucrativos = ''
        for indice in lucro_list:
            caminhos_lucrativos += str(job[indice].path)
            print("Para :", job[indice].path[0][-1], "Path : ", job[indice].path[0], "Com lucro = ", job[indice].profit)
            print("Tempo de início : ",job[indice].start, " e tempo final ", job[indice].finish)
        print("Totalizando : ", lucro_max," de lucro")
        print(caminhos_lucrativos)
        graph.clear()
        entregas.clear()

