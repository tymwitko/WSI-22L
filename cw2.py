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
    # x_a, o_a = best(P, orate)
    while True:
        R = select(P, orate, μ )
        M = cross_mut(R, pm, pc )
        orate = rate( q, M )
        # x, o = best( M, orate)
        # if o <= o_a:
            # o_a = o
            # x_a = x
        P = M
        t = t + 1
        # dodac warunek stopu!
    return P, orate

def select(P, o, μ):
    pass

def rate(q, P):
    tab = []
    for i in P:
        tab.append(q(i))
    return tab

# def best(P, o, μ):
#     pass

def cross_mut(R, pm, pc):
    pass

if __name__ == "__main__":
    tiem = 200
    h_init = 0
    goal = 750
