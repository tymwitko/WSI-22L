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

def d_height(fuel, engine):
    # zmiana wysokosci w jednostce czasu
    a_sum = acc_up(fuel, engine) + gravity_down()
    v = a_sum * 1
    a_sum += fric_down(v, 20 + fuel)

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

def genetic(q, P, μ, pm, pc, tmax):
    '''
    q - funkcja celu
    P - populacja poczatkowa
    μ - liczebnosc populacji
    pm - prawdopodobienstwo mutacji
    pc - prawdopodobienstwo krzyzowania
    '''
    t = 0
    orate = rate( q, P )
    while True:
        R = select(P, orate, μ )
        M = cross_mut(R, pm, pc )
        orate = rate( q, M )
        P = M
        t = t + 1
        # dodac warunek stopu!
    return P, orate

def probability(P, unit):
    if pattern in P:
        return height(unit)/sum_goal(P)

def sum_goal(P):
    summ = 0
    for pattern in P:
        summ += goal_func(height(pattern), sum(pattern))
    return summ

def select(P, o, μ):
    weights = []
    for i in range(len(P)):
        weights.append(probability(P, P[i]))
    return random.choices(P, weights, None, len(P)-1) # TODO: jak dobierać liczebność populacji po selekcji (tu len(P)-1)? Czy to element zadania?

def rate(q, P):
    tab = []
    for i in P:
        tab.append(q(i))
    return tab

def cross_mut(R, pm, pc):
    temp = cross(R, pc)
    temp = mut(temp, pm)

def cross(P, pc):
    for pattern in P:
        if random.random() <= pc:
            point = random.randrange(len(pattern))
            temp = pattern[point:] #TODO: jak dobierać drugi? czy mogą się powtarzać?

def mut(P, pm):
    for pattern in P:
        for unit in pattern:
            if random.random() <= pm:
                if unit == 1:
                    unit = 0
                else:
                    unit = 1
    return P

if __name__ == "__main__":
    tiem = 200
    h_init = 0
    goal = 750
