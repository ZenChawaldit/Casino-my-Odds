
###Libraries
import sys
import numpy as np
import math

### decision tree data structure
class Node:
    def __init__(self, attributes, index, depth, data):
        self.left = None
        self.right = None
        self.att_used = attributes #list of indexs used
        self.index = index #or value if leaf
        self.depth = depth #current depth of tree
        self.data = data #2d subset data


##file IO and cleaning data

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

##helper functions for training data

# P(Y = y)
def P(data, Y, y):
    row = data.shape[0]
    count = 0
    for i in range(row):
        if data[i][Y] == y:
            count += 1
    return count / row

# P(Y = y | X = x)
def P_cond(data, Y, y, X, x):
    row = data.shape[0]
    row_cond = []
    #get rows with given x value
    for i in range(row):
        if data[i][X] == x:
            row_cond.append(i)
    if len(row_cond) == 0: return 0
    count = 0
    for j in row_cond:
        if data[j][Y] == y:
            count += 1
    return count / len(row_cond)

def get_possible_values(data, X):
    return list(set(data[:,X]))

def sum_product(L1, L2):
    assert(len(L1) == len(L2))
    result = 0
    for i in range(len(L1)):
        result += L1[i] * L2[i]
    return result

#H(Y) Y is the index
def entropy(data, Y):
    #-sigma (P(Y = y)log2(P(Y=y)))
    (row, col) = data.shape
    values = get_possible_values(data, Y) #[0,1]
    probs = [P(data, Y, i) for i in values]
    log2_probs = []
    for j in probs:
        if j == 0:
            log2_probs.append(0)
        else:
            log2_probs.append(math.log2(j))
    return -sum_product(probs, log2_probs)

# H(Y | X = x)
def entropy_cond_spec(data, Y, X, x):
    (row, col) = data.shape
    values = get_possible_values(data, Y)
    probs = [P_cond(data, Y, i, X, x) for i in values]
    log2_probs = []
    for j in probs:
        if j == 0:
            log2_probs.append(0)
        else:
            log2_probs.append(math.log2(j))
    return -sum_product(probs, log2_probs)

#H(Y|X)
def entropy_cond(data, Y, X):
    values = get_possible_values(data, X)
    probs = [P(data, X, i) for i in values]
    H_probs = [entropy_cond_spec(data, Y, X, i) for i in values]
    return sum_product(probs, H_probs)

# I(Y : X)
def mutual_information(data, Y, X):
    return entropy(data, Y) - entropy_cond(data, Y, X)

#return index to split
def get_split(data, Y, att_used):
    d = dict()
    max_value = -1
    cols = data.shape[1]
    for i in range(cols-1):
        if i in att_used:
            continue
        info = mutual_information(data[1:][:], Y, i)
        if info > max_value: max_value = info
        d[info] = i
    return d[max_value]


#returns list of subsets 
#
def split_data(data, X):
    header = data[0]
    data = data[1:][:]
    values = get_possible_values(data, X)
    row, col = data.shape
    result = []
    for v in values:
        subset = np.empty((0, col))
        for i in range(row):
            if v == data[i][X]:
                subset = np.vstack([subset, data[i]])
        subset = np.vstack((header,subset))
        result.append(subset)
    return result #list of subsets
 
#return the majority output with labels, if even, choose the higher lexicon
def majority(data):
    output_idx = len(data[0]) - 1
    output_data = [i[output_idx] for i in data[1:][:]] #list of outputs
    max_count = -1
    max_value = ''
    values = set(output_data)
    for value in values:
        c = output_data.count(value)
        if c > max_count:
            max_count = c
            max_value = value
        elif c == max_count:
            max_value = max(value, max_value)
    return max_value

def train(data, cur_depth, max_depth, att_used, att):
    row, col = data.shape #with labels
    #base case: max depth reached or no attributes left
    if (max_depth == cur_depth) or (len(att_used) == att):
        value = majority(data) #return majority of Y
        a = Node(att_used, value, cur_depth, data)
        return a
    #base case 2: fully classified or mutual info = 0
    #count = np.count_nonzero(data[1:][:] == instance, axis = 0)[col-1]
    instance = data[1][col-1]
    index = get_split(data[1:][:], col-1, att_used) #get index to split
    Y = data.shape[1]-1
    if (mutual_information(data[1:][:], Y,index) == 0):
        a = Node(att_used, instance, cur_depth, data)
        return a
    ##recursive branch case return branch initialize node
    #get attribute to split
    #create new tree 
    branch = Node(att_used, index, cur_depth, data)
    #create children

    ##DEEPCOPY
    att_used = att_used + []
    att_used.append(index)
    cur_depth += 1
    (data_left, data_right) = split_data(data, index) #split data only gives one
    branch.left = train(data_left, cur_depth, max_depth, att_used, att)
    branch.right = train(data_right, cur_depth, max_depth, att_used, att)
    return branch


#outputs a tree for making decision
def decisionTreeTrain(D, max_depth):
    cur_depth = 0
    row, col = D.shape
    att = col - 1
    att_used = [] #attribute used
    return train(D, cur_depth, max_depth, att_used, att)


def predict(row, tree):
    #leaf, return index
    if tree.left == None and tree.right == None:
        return tree.index
    #branch, go to the next, left or right
    value = row[tree.index]
    #edge
    edge = tree.left.data[1][tree.index]
    if value == edge:
        return predict(row, tree.left)
    else:
        return predict(row, tree.right)


#given data and tree predict the outcome, return list of predictions
def test(data, tree):
    result =[]
    data = data[1:][:]
    row = data.shape[0]
    for i in range(row):
        p = predict(data[i], tree)
        result.append(p)

    return result

#get error rate
def error(data, predictions):
    row, col = data.shape
    correct = 0
    for i in range(1, row):
        output_idx = col - 1
        if data[i][output_idx] == predictions[i-1]:
            correct += 1
    return 1 - (correct / (row-1))

#print tree in dfs order
def print_tree(tree, depth, instance1, instance2):
    #base case: leaf
    if tree == None:
        return
    #recursive
    depth_text = "| " * depth

    #attribute, instance
    if tree.depth == 0:
        name_text = ""
    else:
        attribute_col = tree.att_used[tree.depth - 1]
        attribute = tree.data[0][attribute_col]
        instance = tree.data[1][attribute_col]
        name_text = f"{attribute} = {instance}: "
    #statistic
    d_set = list(tree.data[1:,-1])
    num1, num2 = d_set.count(instance1), d_set.count(instance2)    
    
    stat_text = f"[{num1} {instance1}/{num2} {instance2} ]"
    text = depth_text + name_text + stat_text
    print(text)

    print_tree(tree.left, depth + 1, instance1, instance2)
    print_tree(tree.right, depth + 1, instance1, instance2)
    return

def main():
    #store io path
    train_i_path = sys.argv[1]
    test_i_path = sys.argv[2]
    max_depth = sys.argv[3] #max depth
    train_o_path = sys.argv[4]
    test_o_path = sys.argv[5]
    metric_o_path = sys.argv[6]

    #accessing/parsing input content
    train_i = readFile(train_i_path)
    test_i = readFile(test_i_path)
    D_train = np.array(get_2d_list(train_i))
    D_test = np.array(get_2d_list(test_i))
    depth = int(float((max_depth)))
    
    #computation
    tree = decisionTreeTrain(D_train, depth)
    
    #storing the output
    trained = test(D_train, tree)
    writeFile(train_o_path, "\n".join(trained))

    tested = test(D_test, tree)
    writeFile(test_o_path, "\n".join(tested))

    #give error rate for both
    erate_train = error(D_train , trained)
    erate_test = error(D_test, tested)
    error_text = "error(train): %f\nerror(test): %f" % (erate_train, erate_test)
    writeFile(metric_o_path, error_text)    

    #print out the tree
    instance1, instance2 = get_possible_values(D_train[1:][:], D_train.shape[1]-1)
    print_tree(tree, 0, instance1, instance2)
    return

if __name__ == '__main__':
    main()