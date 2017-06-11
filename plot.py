import operator
import numpy as np
import matplotlib.pyplot as plt

#======Pre-define helper functions=========


#======================END===================

def plotChangeIndexToKeyIndex(code_change_map, line_set_string, length=0):
    sortByKey = sorted(code_change_map.items(), key=operator.itemgetter(0), reverse=False)
    key_index =  {}
    i = 0
    for k in sortByKey:
        key_index[k[0]] = i
        i += 1
    
    if length == 0:
        plen = len(sortByKey)
    else:
        plen = length

    #print key_index
    sortByValue = sorted(code_change_map.items(), key=operator.itemgetter(1), reverse=True)
    x = [i for i in range(plen)]
    y = []
    for k in sortByValue:
        y.append(key_index[k[0]])
        if len(y) >= plen:
            break
    print len(x), len(y)
    plt.plot(x, y, line_set_string)
    #plt.show()


if __name__ == "__main__":
    x = [0,1,2,3]
    y = [15,10,16,8]

    plt.scatter(x,y)
    plt.show()