from cmath import inf
import random

import numpy as np


class NoFuelError(Exception):
    pass

class EngineOffError(Exception):
    pass

def goal_func(h, fuel):
    if h >= 150: #750:
        return 200 - fuel
    else:
        return 0

def acc_up(fuel, engine):
    if engine:
        return 500/(20+fuel)
    else:
        return 0

def fric_down(v, m):
    return -0.06 * v * abs(v) / m

def gravity_down():
    return -0.9

def d_height(fuel, engine):
    # zmiana wysokosci w jednostce czasu
    a_sum = acc_up(fuel, engine) + gravity_down()
    v = a_sum * 1
    a_sum += fric_down(v, 20 + fuel)
    v = a_sum * 1
    return v * 1
    

def height(pattern):
    fuel = sum(pattern)
    h = 0
    for i in pattern:
        h += d_height(fuel, i)
        if i:
            fuel -= 1
    return h


# def genetic(pm, pc, mu):
#     pm=0.5 # p mutacji
#     pc=0.5 # p krzyzowania
#     mu=0.5
#     t=0
#     P0 = inicjalizacja() # populacja poczatkowa
#     rate( P0 )
#     while(not end):
#         Tt = selekcja( Pt )
#         Ot = cross_mut( Tt )
#         rate ( Ot )
#         Pt + 1 = Ot
#         t = t+1

def genetic(q, μ, pm, pc, iters, length):
    '''
    q - funkcja celu
    P - populacja poczatkowa
    μ - liczebnosc populacji
    pm - prawdopodobienstwo mutacji
    pc - prawdopodobienstwo krzyzowania
    '''
    t = 0
    Po = popul_init(μ, length)
    orate = rate( q, Po )
    while t < iters:
        Re = select(Po, orate, μ )
        Mu = cross_mut(Re, pm, pc )
        orate = rate( q, Mu )
        Po = Mu
        t = t + 1
    return Po, orate, [height(i) for i in Po]

def probability(P, pattern):
    if pattern in P:
        try:
            return height(pattern)/sum_goal(P)
        except ZeroDivisionError:
            return 0

def sum_goal(P):
    summ = 0
    for pattern in P:
        summ += goal_func(height(pattern), sum(pattern))
    return summ

def select(P, o, μ):
    weights = []
    sel_inds = []
    for i in range(μ):
        weights.append(probability(P, P[i])) # po pewnym czasie same zera
    for i in range(μ):
        sel_inds.append(random.choices(range(0,μ), weights=weights, k=1)[0])
    print(sel_inds)
    print(weights)
    try:
        return [P[i] for i in sel_inds] # liczebność populacji stała, mogą być duplikaty
    except IndexError:
        print("AAAAAAAAAA! " + str(len(P)), len(sel_inds))
        print(P[99])

def rate(q, P):
    tab = []
    for i in P:
        tab.append(q(height(i),sum(i)))
    return tab

def cross_mut(R, pm, pc):
    temp = cross(R, pc)
    temp = mut(temp, pm)
    return temp

def cross(P, pc):
    ind = 0
    crossed = []
    while ind < len(P):
        if random.random() <= pc:
            try:
                point = random.randrange(len(P[ind]))
                temp = P[ind][point:] #jak jest npar to po prostu dobrać jakiegoś powtórzonego i zostawić 1 dziecko
                P[ind][point:] = P[ind+1][point:]
                P[ind+1][point:] = temp
                crossed.append(P[ind])
                crossed.append(P[ind+1])
            except IndexError:
                point = random.randrange(len(P[ind]))
                P[ind][point:] = P[0][point:]
                crossed.append(P[ind][point:])
        else:
            crossed.append(P[ind])
            crossed.append(P[ind+1])
        ind += 2
    return crossed

def mut(P, pm):
    for pattern in P:
        for unit in pattern:
            if random.random() <= pm:
                if unit == 1:
                    unit = 0
                else:
                    unit = 1
    return P

def popul_init(μ, length):
    Po = []
    for _ in range(μ):
        temp = np.random.choice([0, 1], size=(length,))
        Po.append(temp.tolist())
    return Po

if __name__ == "__main__":
    tiem = 10 #200
    h_init = 0
    goal = 750
    iters = 100
    pop_size = 20
    pm = 0.3
    pc = 0.2
    print(genetic(goal_func, pop_size, pm, pc, iters, tiem))
