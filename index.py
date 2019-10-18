import numpy as np
import math
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
        cromossomos.append(shuffle(base))
    for i in range(20):
        cromossomos[i].append(cromossomos[i][0])
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

def darwin(cromossomos, aptidao):
    aptidao_sorted = sorted(aptidao, key = lambda i: (i['fitness']))
    cromossomos_sorted = []
    for i in range(10):
        #print("cidade {} - {}".format(aptidao_sorted[i].get('cidade'), aptidao_sorted[i].get('fitness')))
        city = aptidao_sorted[i].get('cidade')
        cromossomos_sorted.append(cromossomos[city])
        #print(cromossomos_sorted[i])
    return cromossomos_sorted

def roleta(cromossomos):
    pai = []
    mae = []
    prob = []
    for i in range(10):
        for j in range(10 -i):
            prob.append(j)
    for i in range(5):
        indice = prob[np.random.randint(54)]
        pai.append(cromossomos[prob[indice]])
        indice = prob[np.random.randint(54)]
        mae.append(cromossomos[prob[indice]])
    return [pai, mae]

def crossover(pais):
    pai = pais[0]
    mae = pais[1]
    filhos = []
    for i in range(len(pai)):
        p1 = pai[i]
        p2 = mae[i]
        idx = np.random.randint(19)
        pais = crossing(p1, p2, idx)
        p1 = pais[0]
        p2 = pais[1]
        while(True):
            ret = cidadeRepete(p1, idx)
            if ret == -1:
                filhos.append(p1)
                filhos.append(p2)
                break
            pais = crossing(p1, p2, ret)
            p1 = pais[0]
            p2 = pais[1]
    return filhos

def crossing(p1, p2, idx):
    aux = p1[idx]
    p1[idx] = p2[idx]
    p2[idx] = aux
    if idx == 0:
        p1[20] = p1[0]
        p2[20] = p2[0]
    return [p1, p2]

def cidadeRepete(cromossomo, idx):
    for i in range(len(cromossomo)):
        for j in range(len(cromossomo)):
            if cromossomo[i] == cromossomo[j] and idx != i:
                return i
    return -1

def mergeFilhos(a1, a2):
    for i in range(10):
        a1.append(a2[i])
    return a1

def app():
    init_city()
    cromossomos = init_cromossomos()
    for j in range(10000):
        aptidao = []
        for i in range(20):
            aptidao.append({"cidade" : i, "fitness": fitness(cromossomos[i])})
        cromossomos = darwin(cromossomos, aptidao)
        pais = roleta(cromossomos)
        filhos = crossover(pais)
        cromossomos = mergeFilhos(cromossomos, filhos)


app()