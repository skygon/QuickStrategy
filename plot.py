import operator
import numpy as np
import matplotlib.pyplot as plt

#======Pre-define helper functions=========


#======================END===================

def plotChangeIndexToKeyIndex(code_change_map, line_set_string):
    sortByKey = sorted(code_change_map.items(), key=operator.itemgetter(0), reverse=False)
    key_index =  {}
    i = 0
    for k in sortByKey:
        key_index[k[0]] = i
        i += 1
    
    #print key_index
    sortByValue = sorted(code_change_map.items(), key=operator.itemgetter(1), reverse=True)
    x = [i for i in range(len(sortByValue))]
    y = []
    for k in sortByValue:
        y.append(key_index[k[0]])
    
    plt.plot(x, y, line_set_string)
    #plt.show()


if __name__ == "__main__":
    x = [0,1,2,3]
    y = [15,10,16,8]

    plt.scatter(x,y)
    plt.show()