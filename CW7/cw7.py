from sklearn import datasets
import numpy as np
import math

def import_data():
    '''
    import iris data from sklearn datasets
    '''
    data = datasets.load_iris()['data']
    target = datasets.load_iris()['target']
    return data, target

def split(data, split):
    '''
    split data into 2 sets in place marked by split
    '''
    np.random.shuffle(data)
    return data[:split, :], data[split:, :]

def ksplit(data, k):
    '''
    split data into k equal (or almost equal) subsets
    '''
    np.random.shuffle(data)
    indices = []
    subsets = []
    for i in range(k):
        indices.append(len(data/k) * (i+1))
    # subsets = np.split(data, indices)
    for i in range(k):
        print(i*(len(data)/k), (i+1)*len(data)/k)
        print(data[int(i*(len(data)/k)):int((i+1)*len(data)/k), :])
        subsets.append(data[int(i*(len(data)/k)):int((i+1)*len(data)/k), :])
    print(np.shape(subsets))
    return subsets

def avg_dev(data):
    '''
    returns averages and standard deviations for each attribute
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

def get_class_avg_dev(data):
    '''
    sums of averages and standard deviations for each class
    '''
    filtered = {}
    avgdevs = {}
    for i in (data):
        if (i[-1] not in filtered):
            filtered[i[-1]] = []
        filtered[i[-1]].append(i)
    for classValue, instances in filtered.items():
        avgdevs[classValue] = avg_dev(instances)
    # print(avgdevs)
    return avgdevs

def prob(x, avgdev):
    '''
    probability for given class from vector with gauss distribution
    x - parameter value from given vector
    avgdev - parameter average and deviation
    '''
    avg = avgdev[0]
    dev = avgdev[1]
    try:
        return math.exp((-(x-avg)**2)/(2*(dev**2))) / (math.sqrt(2*math.pi) * dev)
    except ZeroDivisionError:
        return 1

def run_tests(avgdevs, test):
    '''
    run tests, duh
    returns list of guesses for each vector in test set
    '''
    # print(avgdevs)
    preds = []
    for i in test:
        result = guess(avgdevs, i)
        preds.append(result)
    return preds

def guess(avgdevs, vector):
    '''
    run alg for single vector
    '''
    best_class = None
    best_prob = -1
    for class_guess, probab in get_probs(avgdevs, vector).items():
        if best_prob == -1 or probab > best_prob:
            best_prob = probab
            best_class = class_guess
    return best_class

def get_probs(avgdevs, vector):
    '''
    returns probabilities for each class for given vector
    avgdevs - average and deviation for each parameter
    '''
    probs = {}
    for param_num, param_ad in avgdevs.items():
        probs[param_num] = 1
        for ind, summar in enumerate(param_ad):
            # print(vector, vector[ind], param_ad)
            probs[param_num] *= prob(vector[ind], summar)
    return probs

def k_test_set(subsets, selected):
    out = []
    for ind, element in enumerate(subsets):
        if ind != selected:
            for row in element:
                out.append(row)
    return out

if __name__ == "__main__":
    data, target = import_data()
    full_data = []
    for ind, i in enumerate(data):
        temp = list(i)
        temp.append(target[ind])
        full_data.append(temp)
    full_data = np.array(full_data)
    
    # tests = full_data[:8, :]
    # print("tests:",tests)
    # # ksplit(tests, 3)
    # print("k", ksplit(tests, 3))

    # for k in range(1, 150):
    #     sm = 0
    #     for j in range(25):
    #         learn, test = split(full_data, k)
    #         guesses = run_tests(get_class_avg_dev(learn), test)
    #         git = 0
    #         for ind, i in enumerate(test):
    #             if i[-1] == guesses[ind]:
    #                 git += 1
    #         sm += (git/float(len(test))) * 100.0
        # print("Learning set size:", k, "Correct guesses:", sm/25, "%")
    
    for k in range (2, 4):
        sm = 0
        subsets = ksplit(full_data, k)
        for m in range(k):
            learn = subsets[m]
            test = k_test_set(subsets, m)
            print(np.shape(test), np.shape(learn), np.shape(subsets))
            for j in range(25):
                # print(m, learn, "bla", test)
                guesses = run_tests(get_class_avg_dev(learn), test)
                git = 0
                niegit = 0
                for ind, i in enumerate(test):
                    if i[-1] == guesses[ind]:
                        git += 1
                    else:
                        niegit += 1
                print("wyniki:", git, niegit)
            # sm += (git/(git + niegit)) * 100.0
        # print("Number of sets:", k, "Correct guesses:", sm/25, "%")
