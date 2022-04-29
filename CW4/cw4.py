import pandas as pd
import math
from anytree import Node, RenderTree

# class Node:

#     def __init__(self, parent = None, children = []):
#         self.children = children
#         self.parent = parent
    
#     def append(self, child):
#         self.children.append(child)

#     def getChildren(self):
#         return self.children

def id3(Y, D, U, class_name, commonClass, parentNode):
    if (U[class_name] == U[class_name][0]).all():
        return Lisc_z_klasa_U[class_name][0]
    if len(D) == 0:
        most_freq = commonClass(U[class_name])
        return Lisc_z_most_freq
    d = maxArg(D, U)
    Ubis = {}
    x = []
    for ind in U.shape[0]: # x - 9 wartosci wejsciowych, y - klasa
        for col_name in U:
            # if col_name != class_name:
            #     x.append(U[col_name][ind])
            U = divide(U)
            if x[d] == d[j]: #TODO - co to wgl jest
                Ubis[j].append((x, y))
    # for tree in Ubis: # nie tak, ale cos trzeba z tym iterowaniem po wezlach zrobic
    #     Node(tree, parent = U)
    return Drzewo_z_korzeniem_d_i_krawedziami_dj_prowadzacymi_do_drzew_z_Ubisami

def maxArg(D, U):
    arg = D[0]
    gain = infGain(D[0], U)
    for d in D:
        if infGain(d, U) >= gain:
            gain = infGain(d, U)
            arg = d
    return arg

def infGain(d, U):
    return i(U) - info(d, U)

def i(U, class_name):
    sumka = 0
    freqs = classFreqs(U, U[class_name])
    for fi in freqs:
        sumka += fi * math.log(fi)
    return sumka

# def allClassFreqs(U):
#     freqs = {}
#     for col_name in U:
#         freqs[col_name] = classFreqs(col_name)
#     return freqs

def info(d, U, class_name):
    divided = divide(d, U)
    sumka = 0
    for Uj in divided:
        sumka += float(len(Uj))/float(len(U)) * i(U, class_name)

def divide(d, U): # d - nazwa kolumny, wg ktorej dzielimy
    return [y for _, y in U.groupby(d, as_index=False)]

def commonClass(class_col):
    names = getClassValues(class_col)
    counts = {}
    for i in names:
        counts[i] = 0
    for i in class_col:
        counts[i] += 1
    return [*dict(sorted(counts.items(), key=lambda item: item[1]))][len(counts)-1]

def classFreqs(class_col):
    names = getClassValues(class_col)
    counts = {}
    for i in names:
        counts[i] = 0
    for i in class_col:
        counts[i] += 1
    return counts

def importData(filename):
    data = pd.read_csv(filename, sep=",")
    return data

def getClassValues(class_col):
    values = []
    for i in class_col:
        if i not in values:
            values.append(i)
    return values

def getEntryValues(entry_data):
    entry_vals = {}
    for column_name in entry_data:
        entry_vals[column_name] = getClassValues(entry_data[column_name])
    return entry_vals

def split(data, split1, split2):
    return data.iloc[:split1, :], data.iloc[split1:split2, :], data.iloc[split2:, :]


if __name__ == "__main__":
    filename = "CW4/breast-cancer.data"
    data = importData(filename)
    print(getClassValues(data['irradiat']))
    print(getEntryValues(data.iloc[:, :9]))
    # print(id3(getClassValues(data["irradiat"]), getEntryValues(data, "irradiat")))
    print(data.iloc[:5, :])
    print(commonClass(data["tumor-size"]))
    print(divide('irradiat', data))
    for y in data:
        print(" y: ", y)
    drzewo = Node("x1")
    lisc = Node("x2", parent=drzewo)
    for pre, fill, node in RenderTree(drzewo):
        print("%s%s" % (pre, node.name))
