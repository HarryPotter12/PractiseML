#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 23:42:33 2020

@author: Anuran Banerjee
"""
# CS6510 HW 1 Code Skeleton
# Please use this outline to implement your decision tree. You can add any code around this.

import csv
import math
import random

# Enter You Name Here
myname = "Anuran-Banerjee-" # or "Doe-Jane-"

# Implement your decision tree below
class DecisionTree():
    tree = {}

    def learn(self, training_set, attributes, target):
        # implement this function
        self.tree = build_tree(training_set, attributes, target)

# Class Node which will be used while classify a test-instance using the tree which was built earlier
class Node():
    value = ""
    children = []

    def __init__(self, val, dictionary):
        self.value = val
        if (isinstance(dictionary, dict)):
            self.children = list(dictionary)

# Majority Function which tells which class has more entries in given data-set
def majorClass(attributes, data, target):

    freq = {}
    index = attributes.index(target)

    for tuple in data:
        if tuple[index] in freq:
            freq[tuple[index]] += 1 
        else:
            freq[tuple[index]] = 1

    max = 0
    major = ""

    for key in list(freq):
        if freq[key]>max:
            max = freq[key]
            major = key

    return major


# Calculates the entropy of the data given the target attribute
def entropy(attributes, data, targetAttr):

    freq = {}
    dataEntropy = 0.0

    i = 0
    for entry in attributes:
        if (targetAttr == entry):
            break
        i = i + 1

    i = i - 1

    for entry in data:
        if entry[i] in freq:
            freq[entry[i]] += 1.0
        else:
            freq[entry[i]]  = 1.0

    for freq in freq.values():
        dataEntropy += (-freq/len(data)) * math.log(freq/len(data), 2) 
        
    return dataEntropy


# Calculates the information gain (reduction in entropy) in the data 
# when a particular attribute is chosen for splitting the data.
def info_gain(attributes, data, attr, targetAttr):

    freq = {}
    subsetEntropy = 0.0
    i = attributes.index(attr)

    for entry in data:
        if entry[i] in freq:
            freq[entry[i]] += 1.0
        else:
            freq[entry[i]]  = 1.0

    for val in list(freq):
        valProb        = freq[val] / sum(freq.values())
        dataSubset     = [entry for entry in data if entry[i] == val]
        subsetEntropy += valProb * entropy(attributes, dataSubset, targetAttr)

    return (entropy(attributes, data, targetAttr) - subsetEntropy)


# This function chooses the attribute among the remaining attributes which has the maximum information gain.
def attr_choose(data, attributes, target):

    best = attributes[0]
    maxGain = 0;

    for attr in attributes:
        newGain = info_gain(attributes, data, attr, target) 
        if newGain>maxGain:
            maxGain = newGain
            best = attr

    return best


# This function will get unique values for that particular attribute from the given data
def get_values(data, attributes, attr):

    index = attributes.index(attr)
    values = []

    for entry in data:
        if entry[index] not in values:
            values.append(entry[index])

    return values

# This function will get all the rows of the data where the chosen "best" attribute has a value "val"
def get_data(data, attributes, best, val):

    new_data = [[]]
    index = attributes.index(best)

    for entry in data:
        if (entry[index] == val):
            newEntry = []
            for i in range(0,len(entry)):
                if(i != index):
                    newEntry.append(entry[i])
            new_data.append(newEntry)

    new_data.remove([])    
    return new_data


# This function is used to build the decision tree using the given data, 
# attributes and the target attributes. It returns the decision tree in the end.
def build_tree(data, attributes, target):

    data = data[:]
    vals = [record[attributes.index(target)] for record in data]
    default = majorClass(attributes, data, target)

    if not data or (len(attributes) - 1) <= 0:
        return default
    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        best = attr_choose(data, attributes, target)
        tree = {best:{}}
    
        for val in get_values(data, attributes, best):
            new_data = get_data(data, attributes, best, val)
            newAttr = attributes[:]
            newAttr.remove(best)
            subtree = build_tree(new_data, newAttr, target)
            tree[best][val] = subtree
    
    return tree

def run_decision_tree():

    # Load data set
    with open("wine-dataset.csv") as f:
        attrib = next(f, None)
        data = [tuple(line) for line in csv.reader(f, delimiter=",")]
    print("Number of records: %d\n" % len(data))

    # Writing results to a file 
    f = open(myname+"result.txt", "w")
    f.write("Number of records: %d\n\n" % len(data))
    f.close()
    
    attributes = attrib.split(",")
    target = attributes[-1]
    
    # Split training/test sets
    # You need to modify the following code for cross validation.
    K = 10
    training_set = [x for i, x in enumerate(data) if i % K != 9]
    test_set = [x for i, x in enumerate(data) if i % K == 9]
    
    tree = DecisionTree()
    # Construct a tree using training set
    tree.learn( training_set, attributes , target )

    # Classify the test set using the tree we just constructed
    results = []
    for instance in test_set:
        tempDict = tree.tree.copy()
        result = ""
        while(isinstance(tempDict, dict)):
            root = Node(list(tempDict)[0], tempDict[list(tempDict)[0]])
            tempDict = tempDict[list(tempDict)[0]]
            index = attributes.index(root.value)
            value = instance[index]
            if(value in list(tempDict)):
                child = Node(value, tempDict[value])
                result = tempDict[value]
                tempDict = tempDict[value]
            else:
                result = "Null"
                break
        if result != "Null":
            results.append(result == instance[-1])
            
    # Accuracy
    accuracy = float(results.count(True))/float(len(results))
    print("=== Initial Implementation ===")
    print("Accuracy: %.4f\n" % accuracy)
    print("=== Cross-validation ===")
    
    # Writing results to a file 
    f = open(myname+"result.txt", "a")
    f.write("=== Initial Implementation === \n")
    f.write("Accuracy: %.4f\n\n" % accuracy)
    f.write("=== Cross-validation === \n")
    f.close()
    
    K = 10
    acc = []
    for k in range(K):
        # random.seed(42)
        # random.shuffle(data)
        training_set = [x for i, x in enumerate(data) if i % K != k]
        test_set = [x for i, x in enumerate(data) if i % K == k]
        tree = DecisionTree()
        tree.learn( training_set, attributes, target )
        results = []

        for entry in test_set:
            tempDict = tree.tree.copy()
            result = ""
            while(isinstance(tempDict, dict)):
                root = Node(list(tempDict)[0], tempDict[list(tempDict)[0]])
                tempDict = tempDict[list(tempDict)[0]]
                index = attributes.index(root.value)
                value = entry[index]
                if(value in list(tempDict)):
                    child = Node(value, tempDict[value])
                    result = tempDict[value]
                    tempDict = tempDict[value]
                else:
                    result = "Null"
                    break
            if result != "Null":
                results.append(result == entry[-1])

        accuracy = float(results.count(True))/float(len(results))

        print("%d-th fold Accuracy: %.4f" % (k+1, accuracy))
        f = open(myname+"result.txt", "a")
        f.write("%d-th fold Accuracy: %.4f\n" % (k+1, accuracy))
        f.close()
        acc.append(accuracy)
    
    # Average Accuracy
    avg_acc = sum(acc)/len(acc)
    print("\n=== After Cross-validation ===")
    print("Average accuracy: %.4f" % avg_acc)    

    # Writing results to a file
    f = open(myname+"result.txt", "a")
    f.write("\n=== After Cross-validation === \n")
    f.write("Average accuracy: %.4f\n" % avg_acc)
    f.close()


if __name__ == "__main__":
    run_decision_tree()
