# Tymon Kobylecki WSI 22L

from inspect import signature
import math

def f(x):
    return x**4

def df(x):
    return [4 * x[0]**3]

def g(args):
    return 1.5 - math.exp(-args[0]**2 - args[1]**2) - 0.5 * math.exp(-(args[0] - 1)**2 - (args[1] + 2)**2)

def dg(args):
    d1 = 2 * args[0] * math.exp(-args[0]**2 - args[1]**2) + (args[0] - 1) * math.exp(-(args[0] - 1)**2 - (args[1] + 2)**2)
    d2 = 2 * args[1] * math.exp(-args[0]**2 - args[1]**2) + (args[1] + 2) * math.exp(-(args[0] - 1)**2 - (args[1] + 2)**2)
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

def gradient(dfunc, beta, args):
    dargs = dfunc(args)
    for i in range(len(dargs)):
        args[i] -= beta * dargs[i]
        print("x" + str(i+1) + " = " + str(args[i]))
    print("---------------")
    return args, dargs
    

if __name__ == "__main__":
    (func, x1, x2, beta, tol) = collect_inputs()
    if func == "f":
        func = df
    elif func == "g":
        func = dg
    steps = 0
    while True:
        steps += 1
        try:
            if func == df:
                ([x1], [d1]) = gradient(func, beta, [x1])
            elif func == dg:
                ([x1, x2], [d1, d2]) = gradient(func, beta, [x1, x2])
            if abs(d1) <= tol:
                if func == df:
                    print ("Minimum found in " + str(steps) + " steps")
                    print("x = " + str(x1) + "\ny = " + str(f(x1)))
                    break
                elif func == dg:
                    if abs(d2) <= tol:
                        print ("Minimum found in " + str(steps) + " steps")
                        print("x1 = " + str(x1) + "\nx2 = " + str(x2) + "\ny = " + str(g([x1, x2])))
                        break
        except OverflowError:
            print ("Overflow Error! Decrease the beta parameter or change the initial point.")
            break
