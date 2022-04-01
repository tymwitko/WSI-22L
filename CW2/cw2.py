# Tymon Kobylecki WSI22L

from cmath import inf
import random

import numpy as np


class NoFuelError(Exception):
    pass

class EngineOffError(Exception):
    pass

def goal_func(h, fuel):
    if h >= 750:
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

def d_height(fuel, engine, vinit):
    # zmiana wysokosci w jednostce czasu
    a_sum = acc_up(fuel, engine) + gravity_down()
    v = vinit + a_sum
    a_sum += fric_down(v, 20 + fuel)
    v = vinit + a_sum
    return vinit + a_sum/2, v
    

def height(pattern):
    fuel = sum(pattern)
    h = 0
    v = 0
    for i in pattern:
        h += d_height(fuel, i, v)[0]
        v = d_height(fuel, i, v)[1]
        if i:
            fuel -= 1
    return h

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
    while t < iters:
        Re = select(Po, μ )
        Mu = cross_mut(Re, pm, pc )
        Po = Mu
        t = t + 1
    best = -inf
    best_pat = []
    for pattern in Po:
        if q(height(pattern), sum(pattern)) > best:
            best = q(height(pattern), sum(pattern))
            best_pat = pattern
    return best_pat, best
    # return Po, orate, [height(i) for i in Po]

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

def select(P, μ):
    weights = []
    sel_inds = []
    for i in range(μ):
        weights.append(probability(P, P[i]))
    if sum(weights) == 0:
        for i in range(len(weights)):
            weights[i] = 1
    for i in range(μ):
        sel_inds.append(random.choices(range(0,μ), weights=weights, k=1)[0])
    return [P[i] for i in sel_inds]

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
                temp = P[ind][point:]
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
            try:
                crossed.append(P[ind+1])
            except IndexError:
                pass
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
    tiem = 200
    iters = 2
    pop_size = 500
    pm = 0.001
    pc = 0.001
    for i in range(25):
        print(genetic(goal_func, pop_size, pm, pc, iters, tiem)[1]) 
