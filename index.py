import numpy as np
import math
import copy as cp
import matplotlib.pyplot as plt
from sklearn.utils import shuffle

cities = []

def getPosition():
    return np.random.rand()

def init_city():
    global cities
    for x in range(20):
        city = [getPosition(), getPosition()]
        cities.append(city)

def init_cromossomos():
    base = []
    cromossomos = []
    for i in range(1,21):
        base.append(i)
    for i in range(20):
        cromossomos.append(cp.copy(shuffle(base)))
    for i in range(20):
        cromossomos[i].append(cp.copy(cromossomos[i][0]))
        # for j in range(21): 
            # print("cromosso {},{}: {}".format(i,j,cromossomos[i][j]))
    return cromossomos

def dist_euclidiana(p1, p2):
	p1, p2 = np.array(p1), np.array(p2)
	diff = p1 - p2
	quad_dist = np.dot(diff, diff)
	return math.sqrt(quad_dist)

def fitness(cromossomo):
    global cities
    dist = 0
    for i in range(20):
        p1 = cities[cromossomo[i] - 1]
        p2 = cities[cromossomo[i + 1] - 1]
        dist += dist_euclidiana(p1, p2)
    return dist

def ordena(cromossomos, aptidao):
    #ordena os cromossomos por ordem de aptidão e rotorna apenas os 10 primeiros
    print("Ordenação")
    aptidao_sorted = sorted(aptidao, key = lambda i: (i['fitness']))
    cromossomos_sorted = []
    for i in range(10):
        #print("cidade {} - {}".format(aptidao_sorted[i].get('cidade'), aptidao_sorted[i].get('fitness')))
        city = aptidao_sorted[i].get('cidade')
        print("cromosso before 20")
        print(cromossomos[city])
        del cromossomos[city][20]
        print("cromosso after 20")
        print(cromossomos[city])
        cromossomos_sorted.append(cp.copy(cromossomos[city]))
        #print(cromossomos_sorted[i])
    return cromossomos_sorted

def roleta(cromossomos):
    print("Roleta")
    pai = []
    mae = []
    prob = []
    for i in range(10):
        for j in range(10 -i):
            prob.append(j)
    for i in range(5):
        indice = prob[np.random.randint(54)]
        pai.append(cp.copy(cromossomos[prob[indice]]))
        indice = prob[np.random.randint(54)]
        mae.append(cp.copy(cromossomos[prob[indice]]))
    return [pai, mae]

def crossover(pais):
    print("Crossover")
    pai = pais[0]
    mae = pais[1]
    filhos = []
    for i in range(len(pai)):
        #para cada par de pais gera dois filhotes
        print(" cross", i)
        p1 = pai[i]
        p2 = mae[i]
        idx = np.random.randint(19)
        #primeira troca
        pais = crossing(p1, p2, idx)
        p1 = pais[0]
        p2 = pais[1]
        crossed_idxs = []
        #salvo os indices que ja sofreram troca
        crossed_idxs.append(idx)
        while(True):
            print("cross {} iterando".format(i))
            ret = cidadeRepete(p1, crossed_idxs)
            crossed_idxs.append(ret)
            print(p1)
            print(ret)
            if ret == -1:
                #sem repetição no cromossomo -> adiciono como filhos e paro a recombinação
                filhos.append(cp.copy(p1))
                filhos.append(cp.copy(p2))
                break
            pais = crossing(p1, p2, ret)
            p1 = pais[0]
            p2 = pais[1]
    return filhos

def crossing(p1, p2, idx):
    #print("Crossing")
    aux = p1[idx]
    p1[idx] = p2[idx]
    p2[idx] = aux
    return [p1, p2]

def cidadeRepete(cromossomo, crossed_idxs):
    #procura por repetição no cromossomo que não seja em uma das posições ja trocadas
    #caso não haja repetição retorna -1
    for i in range(len(cromossomo)):
        for j in range(len(cromossomo)):
            if (cromossomo[i] == cromossomo[j]) and (doesntContain(crossed_idxs, j)) and (i != j):
                return j
    return -1

def doesntContain(lista, indice):
    #verifica se o indice está contido na lista
    return not (indice in lista)

def mergeFilhos(cromossomos, filhos):
    #adiciona os filhos gerados a lista
    for i in range(10):
        cromossomos.append(cp.copy(filhos[i]))
    return cromossomos

def removeLastGenoma(cromossomo):
    #Removendo a cidade de retorno para não ter problemas no crossover
    print("remove last genoma")
    pai = cromossomo[0]
    mae = cromossomo[1]
    del pai[20] 
    del mae[20]
    return [pai, mae]

def addLastGenoma(cromossomos):
    #copiando a primeira cidade para a ultima posição
    print("add last genoma")
    for i in range(len(cromossomos)):
        print(cromossomos[i])
    for i in range(20):
        print("last: ------------------------------ i : ", i)
        print(cromossomos[i][0])
        print("cromosso")
        print(cromossomos[i])
        cromossomos[i].append(cp.copy(cromossomos[i][0]))
        print("result")
        print(cromossomos[i])
    return cromossomos

def app():
    init_city()
    cromossomos = init_cromossomos()
    for j in range(10):
        print("Iteração {}".format(j))
        aptidao = []
        for i in range(20):
            aptidao.append({"cidade" : i, "fitness": fitness(cromossomos[i])})
        cromossomos = ordena(cromossomos, aptidao)
        pais = roleta(cromossomos)
        #print("pais")
        #for k in range(len(pais[0])):
        #    print(pais[0][k])
        #print("maes")
        #for k in range(len(pais[1])):
        #    print(pais[1][k])
        filhos = crossover(pais)
        #print("final")
        #for k in range(len(cromossomos)):
        #    print(cromossomos[k])
        cromossomos = mergeFilhos(cromossomos, filhos)
        #print("filhos")
        #for k in range(len(filhos)):
        #    print(filhos[k])
        #print("final")
        for k in range(len(cromossomos)):
            print(cromossomos[k])
        cromossomos = addLastGenoma(cromossomos)
    print("tamanho da população: ", len(cromossomos))
    print("cidades: ", len(cities))
    #print cities para ver o mapa das cidades
    #print(cities)
    print("melhor custo: ", fitness(cromossomos[0]))
    print("melhor solução: {}".format(cromossomos[0]))

app()