import os
import Queue
import threading

# global variables
file_path = ".\detail_data"
SHA = ".\config\sh_a.txt"
SZA = '.\config\sz_a.txt'

thread_pool_num = 10

#analysis queue. Should be the all codes
analysis_queue = Queue.Queue()


#===============================Helper functions========================================
def usage():
    print '''
    usage:
    python autoDownload.py date_string
    example : python autoDownload.py "2017-05-18"
    '''

def read_to_queue(prefix, filename):
    f = open(filename)
    line = f.readline()
    while line:
        code = prefix + line.strip('\n')
        analysis_queue.put(code)
        line = f.readline()
    f.close()

def init_analysis_queue():
    # read codes from files
    read_to_queue('sh', SHA)
    read_to_queue('sz', SZA)


def mylogger(message, vars):
    print message %(vars)
#===============================End of helper functions=================================


