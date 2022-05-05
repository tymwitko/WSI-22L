# Tymon Kobylecki WSI 22L

import pandas as pd
import math
from anytree import Node, RenderTree, NodeMixin, LevelOrderIter
from copy import deepcopy
import sys

drzewo = None

class MyNode(NodeMixin):
    '''
    tree node with name (value), col_name and parentval which connects the parent to the child
    '''
    def __init__(self, name, col_name, parentval="", parent=None):
        super(MyNode, self).__init__()
        self.name = name
        self.col_name = col_name
        self.parent = parent
        self.parentval = parentval

def is_equal(s):
    '''
    checks whether all values in column s are equal
    '''
    a = s.to_numpy()
    return (a[0] == a).all()

def id3(Y, D, U, class_name, commonClass, MyNode, depth=math.inf, parentNode=None, parent_val=None): # D to nazwy klas wejściowych
    if len(D) == 0 or depth <= 0:
        most_freq = commonClass(U[class_name])
        node = MyNode(most_freq, class_name, parent_val, parent=parentNode)
        return node
    if is_equal(U[class_name]):
        node = MyNode(U[class_name].iloc[0], class_name, parent_val, parent=parentNode)
        return node
    d = maxArg(D, U, class_name)
    copy = deepcopy(D)
    copy.pop(d, None)
    nodes = []
    node = MyNode("", d, parent_val, parent=parentNode)
    for pre, fill, nodee in RenderTree(node):
        treestr = u"%s%s" % (pre, nodee.name)
    for value in getClassValues(U[d]):
        Ubis = U[U[d].isin([value])]
        nodes.append(id3(Y, copy, Ubis, class_name, commonClass, MyNode, depth-1, node, value))
    return node

def maxArg(D, U, class_name):
    '''
    returns arg of maximum information gain
    '''
    arg = None
    gain = None #infGain(D[0], U)
    for d in D:
        if gain is not None:
            if infGain(d, U, class_name) >= gain or arg == None:
                gain = infGain(d, U, class_name)
                arg = d
        else:
            gain = infGain(d, U, class_name)
            arg = d
    return arg

def infGain(d, U, class_name):
    '''
    information gain
    '''
    return i(U, d) - info(d, U, class_name)

def i(U, class_name):
    sumka = 0
    freqs = classFreqs(U[class_name])
    for fi in freqs:
        sumka += freqs[fi] * math.log(freqs[fi])
    return sumka

def info(d, U, class_name):
    '''
    information
    '''
    divided = divide(d, U)
    sumka = 0
    for Uj in divided:
        sumka += float(len(Uj))/float(len(U)) * i(U, class_name)
    return sumka

def divide(d, U): # d - nazwa kolumny, wg ktorej dzielimy
    '''
    divides dataframe into dataframes by value in column d
    '''
    return [y for _, y in U.groupby(d, as_index=False)]

def commonClass(class_col):
    '''
    returns most common class value from column
    '''
    names = getClassValues(class_col)
    counts = {}
    for i in names:
        counts[i] = 0
    for i in class_col:
        counts[i] += 1
    return [*dict(sorted(counts.items(), key=lambda item: item[1]))][len(counts)-1]

def classFreqs(class_col):
    '''
    returns dict of numbers of occurrances of each value from column
    '''
    names = getClassValues(class_col)
    counts = {}
    for i in names:
        counts[i] = 0
    for i in class_col:
        counts[i] += 1
    return counts

def importData(filename):
    '''
    imports data from csv
    '''
    data = pd.read_csv(filename, sep=",")
    return data

def getClassValues(class_col):
    '''
    gets all possible values from column
    '''
    values = []
    for i in class_col:
        if i not in values:
            values.append(i)
    return values

def getEntryValues(entry_data):
    '''
    returns column values from entry data
    '''
    entry_vals = {}
    for column_name in entry_data:
        entry_vals[column_name] = getClassValues(entry_data[column_name])
    return entry_vals

def split(data, split1, split2):
    '''
    split data into 3 sets in places marked by split1 and split2
    '''
    data = data.sample(frac=1)
    return data.iloc[:split1, :], data.iloc[split1:split2, :], data.iloc[split2:, :]



def guess(ver_row, depth, tree, class_name, real_ans, debug=False):
    root = None
    stop = False
    j = 0
    parent = None
    for i in range(depth+1):
        node_list = []
        for node in LevelOrderIter(drzewo):
            if node.parent == root:
                node_list.append(node)
        for node in node_list:
            if node.col_name == class_name:
                root = node
                break
            if node.parent == root:
                try:
                    if root == None:
                        root = node
                        break
                    if debug:
                        for pre, fill, node in RenderTree(node):
                            if node.parentval != "":
                                treestr = u"%s%s" % (pre, node.parentval)
                                print(treestr.ljust(8), " -> ", node.name, "(", node.col_name, ")")
                            else:
                                treestr = u"%s%s" % (pre, node.name)
                                print(treestr.ljust(8), "(", node.col_name, ")")
                        print(node.parentval, "!=", ver_row[node.parent.col_name])
                    if node.parentval == ver_row[node.parent.col_name]: #TODO: co z niezaobserwowanymi klasami
                        root = node
                        break
                except KeyError:
                    if node.col_name == class_name:
                        root = node
                        break
    if root.name != real_ans and debug:
        print(root.col_name, root.name, real_ans)
    return root.name == real_ans, root.name, real_ans



if __name__ == "__main__":
    filename = "CW4/breast-cancer.data"
    data = None
    try:
        data = importData(filename)
    except FileNotFoundError:
        try:
            filename = "breast-cancer.data"
            data = importData(filename)
        except FileNotFoundError:
            print("File not found! Enter correct filename")
            sys.exit()
    class_name = "irradiat"

    teach, validate, verif = split(data, 95, 190)

    max_accuracy = 0
    test_accuracy = 0
    best_depth = 0

    drzewko = None

    for maxdepth in range(10):
        maxdepth
        drzewo = id3(getClassValues(data[class_name]), getEntryValues(data.iloc[:, :9]), teach, class_name, commonClass, MyNode, maxdepth)

        sumka = 0
        for ind, row in teach.iterrows():
            if guess(row.iloc[:9], maxdepth, drzewo, class_name, row[class_name])[0]:
                sumka += 1

        teachaccuracy = float(sumka)/teach.shape[0]

        sumka = 0
        for ind, row in validate.iterrows():
            if guess(row.iloc[:9], maxdepth, drzewo, class_name, row[class_name])[0]:
                sumka += 1

        accuracy = float(sumka)/validate.shape[0]

        # JA JUZ NIE WIEM CZEMU ALE JAK WYJME TO Z FORA TO NIE DZIALA
        sumka = 0
        for ind, row in verif.iterrows():
            if guess(row.iloc[:9], maxdepth, drzewo, class_name, row[class_name])[0]:
                sumka += 1
        testaccuracy = float(sumka)/verif.shape[0]

        # print(teachaccuracy, accuracy, testaccuracy)

        if accuracy > max_accuracy:
            max_accuracy = accuracy
            best_depth = maxdepth
            drzewko = drzewo
            test_accuracy = testaccuracy
    
    print("Best depth:", best_depth)

    # for pre, fill, node in RenderTree(drzewko):
    #     if node.parentval != "":
    #         treestr = u"%s%s" % (pre, node.parentval)
    #         print(treestr.ljust(8), " -> ", node.name, "(", node.col_name, ")")
    #     else:
    #         treestr = u"%s%s" % (pre, node.name)
    #         print(treestr.ljust(8), "(", node.col_name, ")")

    print("Accuracy with best depth (on validation set):", max_accuracy)

    # O TU NIE DZIALA I NIE WIEM CZEMU
    # sumka = 0
    # for ind, row in verif.iterrows():
    #     if guess(row.iloc[:9], best_depth, drzewko, class_name, row[class_name])[0]:
    #         sumka += 1
    # accuracy = float(sumka)/verif.shape[0]

    print("Accuracy on test set:", test_accuracy)
