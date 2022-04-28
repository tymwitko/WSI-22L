import pandas as pd
import math

def id3(Y, D, U):
    checked = 0
    for (x, y) in U:
        if y == klasa_y:
            checked += 1
    if checked == len(U):
        return Lisc_z_klasa_y
    if len(D) == 0:
        return Lisc_z_najczestsza_klasa_w_U
    d = infGain(max(D), U)
    Uj = []
    for (x, y) in U:
        if x[d] == d[j]:
            Uj.append((x, y))
    return Drzewo_z_korzeniem_d_i_krawedziami_dj_prowadzacymi_do_drzew

def infGain(d, U):
    return i(U) - infi(d, U)

def i(U):
    sumka = 0
    for fi in classFreq(U):
        sumka += fi * math.log(fi)
    return sumka

def classFreq(U):
    pass

def infi(d, U):
    divided = divide(d, U)
    sumka = 0
    for Uj in divided:
        sumka += float(len(Uj))/float(len(U)) * i(U)

def commonClass(class_col):
    names = getClassValues(class_col)
    counts = {}
    for i in names:
        counts[i] = 0
    for i in class_col:
        counts[i] += 1
    return [*dict(sorted(counts.items(), key=lambda item: item[1]))][len(counts)-1]
    # return counts

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