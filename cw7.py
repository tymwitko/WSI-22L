from sklearn import datasets
import numpy as np

def import_data():
    data = datasets.load_iris()['data']
    target = datasets.load_iris()['target']
    return data, target

def split(data, split):
    '''
    split data into 2 sets in place marked by split
    '''
    np.random.shuffle(data)
    # data = data.sample(frac=1)
    return data[:split, :], data[split:, :-1]

if __name__ == "__main__":
    data, target = import_data()
    full_data = []
    for ind, i in enumerate(data):
        print(i, target[ind])
        temp = list(i)
        temp.append(target[ind])
        full_data.append(temp)
    full_data = np.array(full_data)
    # print("full" ,full_data)
    learn, test = split(full_data, 75)
    print(learn)
