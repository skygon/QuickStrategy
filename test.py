import os

f = open('.\config\sz_a.txt')
line = f.readline()

while line:
    print line.strip('\n')
    line = f.readline()
    

f.close()