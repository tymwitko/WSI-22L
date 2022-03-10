# Tymon Kobylecki WSI 22L

import math

def f(x):
    return x**4

def df(x):
    return 4 * x**3

def g(x1, x2):
    return 1.5 - math.exp(-x1**2 - x2**2) - 0.5 * math.exp(-(x1 - 1)**2 - (x2 + 2)**2)

def dg(x1, x2):
    d1 = 2 * x1 * math.exp(-x1**2 - x2**2) + (x1 - 1) * math.exp(-(x1 - 1)**2 - (x2 + 2)**2)
    d2 = 2 * x2 * math.exp(-x1**2 - x2**2) + (x2 + 2) * math.exp(-(x1 - 1)**2 - (x2 + 2)**2)
    return (d1, d2)

def collect_inputs():
    print("Welcome! Select the function (f or g):")
    func = input()
    print("Enter initial point x1:")
    x1 = float(input())
    if func == "g":
        print("Enter initial point x2:")
        x2 = float(input())
    else:
        x2 = 0
    print ("Enter the beta parameter:")
    beta = float(input())
    print("Enter the desired tolerance")
    tol = float(input())
    return func, x1, x2, beta, tol

def gradient(func, x1, beta, x2 = 0):
    if func == "f":
        d1 = df(x1)
        x1 -= beta * d1
        print("x = " + str(x1))
        return x1, d1
    elif func == "g":
        d1 = dg(x1, x2)[0]
        d2 = dg(x1, x2)[1]
        x1 -= beta * d1
        x2 -= beta * d2
        print("x1 = " + str(x1) + ", x2 = " + str(x2) + ", y = " + str(g(x1, x2)) + ", dy = " + str(dg(x1, x2)))
        return x1, d1, x2, d2
    

if __name__ == "__main__":
    (func, x1, x2, beta, tol) = collect_inputs()
    print(dg(1, -2))
    steps = 0
    while True:
        steps += 1
        try:
            if func == "f":
                (x1, d1) = gradient(func, x1, beta)
            elif func == "g":
                (x1, d1, x2, d2) = gradient(func, x1, beta, x2)
            if abs(d1) <= tol:
                if func == "f":
                    print ("Minimum found in " + str(steps) + " steps")
                    print("x = " + str(x1) + "\ny = " + str(f(x1)))
                    break
                elif func == "g":
                    if abs(d2) <= tol:
                        print ("Minimum found in " + str(steps) + " steps")
                        print("x1 = " + str(x1) + "\nx2 = " + str(x2) + "\ny = " + str(g(x2, x2)))
                        break
        except OverflowError:
            print ("Overflow Error! Decrease the beta parameter or change the initial point.")
            break
