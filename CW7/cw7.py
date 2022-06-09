from sklearn import datasets
import numpy as np
import math

def import_data():
    data = datasets.load_iris()['data']
    target = datasets.load_iris()['target']
    return data, target

def split(data, split):
    '''
    split data into 2 sets in place marked by split
    '''
    np.random.shuffle(data)
    return data[:split, :], data[split:, :]

def sum_avg_dev(data):
    '''
    sums up averages and standard deviations for each attribute
    '''
    sums = []
    for attr in zip(*data):
        avg = float(sum(attr))/float(len(attr))
        sumk = 0
        for i in attr:
            sumk += (i-avg)**2
        try:
            dev = math.sqrt(float(sumk)/float((len(attr)-1)))
        except ZeroDivisionError:
            dev = 0
        sums.append((avg, dev))
    sums = sums[:-1]
    return sums

def get_class_sums(data):
    '''
    sums of averages and standard deviations for each class
    '''
    filtered = {}
    sums = {}
    for i in (data):
        if (i[-1] not in filtered):
            filtered[i[-1]] = []
        filtered[i[-1]].append(i)
    for classValue, instances in filtered.items():
        sums[classValue] = sum_avg_dev(instances)
    return sums

def prob(x, summar):
    '''
    probability for given class from vector with gauss distribution
    x - parameter value from given vector
    summar - parameter average and deviation
    '''
    avg = summar[0]
    dev = summar[1]
    try:
        return math.exp((-(x-avg)**2)/(2*(dev**2))) / (math.sqrt(2*math.pi) * dev)
    except ZeroDivisionError:
        return 1

def run_tests(sums, testSet):
    '''
    run tests, duh
    '''
    predictions = []
    for i in test:
        result = guess(sums, i)
        predictions.append(result)
    return predictions

def guess(sums, vector):
    '''
    run alg for single vector
    '''
    probabilities = get_probs(sums, vector)
    bestLabel = None
    bestProb = -1
    for classValue, probability in probabilities.items():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel

def get_probs(sums, vector):
    '''
    returns probabilities for each class for given vector
    '''
    # print(vector)
    probs = {}
    for param_num, param_sums in sums.items():
        probs[param_num] = 1
        for ind, summar in enumerate(param_sums):
            # print(vector, vector[ind], param_sums)
            probs[param_num] *= prob(vector[ind], summar)
    return probs

if __name__ == "__main__":
    data, target = import_data()
    full_data = []
    for ind, i in enumerate(data):
        temp = list(i)
        temp.append(target[ind])
        full_data.append(temp)
    full_data = np.array(full_data)
    

    for k in range(1, 150):
        sm = 0
        for j in range(25):
            learn, test = split(full_data, k)
            guesses = run_tests(get_class_sums(learn), test)
            git = 0
            for ind, i in enumerate(test):
                if i[-1] == guesses[ind]:
                    git += 1
            sm += (git/float(len(test))) * 100.0
        print(k, sm/25)
            # print("Correct guesses:", (git/float(len(test))) * 100.0, "%")
