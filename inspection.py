import sys
import numpy as np
import math
#to run:
#python inspection.py small_train.tsv small_inspect.tsv

############### code copied from #################
# http://www.krivers.net/15112-f18/notes/notes-strings.html#basicFileIO
def readFile(path):
    with open(path, "r") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

#get 2d list from strings of space seperated value
def get_2d_list(s):
    D = []
    L = s.splitlines()
    for i in range(len(L)):
        D.append(L[i].split('\t'))
    return D

# P(Y = y)
def P(data, Y, y):
    row = data.shape[0]
    count = 0
    for i in range(row):
        if data[i][Y] == y:
            count += 1
    return count / row

def get_possible_values(data, X):
    return list(set(data[:,X]))

def sum_product(L1, L2):
    assert(len(L1) == len(L2))
    result = 0
    for i in range(len(L1)):
        result += L1[i] * L2[i]
    return result

#H(Y) Y is the index
def get_entropy(data, Y):
    #-sigma (P(Y = y)log2(P(Y=y)))
    (row, col) = data.shape
    values = get_possible_values(data, Y) #[0,1]
    probs = [ P(data, Y, i) for i in values]
    log2_probs = []
    for j in probs:
        if j == 0:
            log2_probs.append(0)
        else:
            log2_probs.append(math.log2(j))
    return -sum_product(probs, log2_probs)

def get_error(data):
    (row, col) = data.shape
    col_data = list(data[:, col-1]) 
    majority = max(set(col_data), key = col_data.count)
    c = col_data.count(majority)
    return  1 - (c / row)

def main():
    #store io path
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    input_data = readFile(input_path)
    D = get_2d_list(input_data)
    data = np.array(D)[1:,:]
    row,col = data.shape

    #get entropy
    entropy = get_entropy(data, col-1)
    #get error rate
    error_rate = get_error(data)
    content = "entropy: " + str(entropy) + "\n" + "error: " + str(error_rate)
    
    writeFile(output_path, content)

if __name__ == '__main__':
    main()