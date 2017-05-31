import os
import Queue
#===================================Global variables=========================
BUY_STR = '\xc2\xf2\xc5\xcc'
SELL_STR = '\xc2\xf4\xc5\xcc'

SHA = os.path.join(os.getcwd(), "config", "sh_a.txt")
SZA = os.path.join(os.getcwd(), "config", "sz_a.txt")

code_queue = Queue.Queue()
#===============================Big deal related=============================
DEAL_LEVEL = 5
BIG_DEAL = {}
# TODO volume levels
BIG_DEAL['volume'] = {}

# amount levels
BIG_DEAL['amount'] = {}
BIG_DEAL['amount'][0] = 50 * 10000
BIG_DEAL['amount'][1] = 100 * 10000
BIG_DEAL['amount'][2] = 200 * 10000
BIG_DEAL['amount'][3] = 500 * 10000
BIG_DEAL['amount'][4] = 1000 * 10000

#=======================Enums========================================
def enum(**enums):
    return type('Enum', (), enums)

DealType = enum(BUY = 1, SELL = 2, UNKNOW = 3)

#================================Invalid code========================================================
invalid_code_file = os.path.join(os.getcwd(), "config", "invalid_code.txt")
invalid_code = []
with open(invalid_code_file) as f:
    line = f.readline()
    while line:
        invalid_code.append(line.strip('\n'))
        line = f.readline()

#print invalid_code

def isInvalidCode(code):
    if code in invalid_code:
        return True
    
    return False


#===============================Code total volumn============================================================
code_volumn_file = os.path.join(os.getcwd(), "config", "code_volumn.csv")
code_volumn = {}
with open(code_volumn_file) as f:
    line = f.readline()
    while line:
        s = line.strip('\n').split(',')
        code_volumn[s[0]] = s[1]
        line = f.readline()

#==========================Helper functions========================================================
def read_to_queue(prefix, filename, dest_queue):
    f = open(filename)
    line = f.readline()
    while line:
        if isInvalidCode(line.strip('\n')):
            line = f.readline()
            continue
        code = prefix + line.strip('\n')
        dest_queue.put(code)
        line = f.readline()
    f.close()

read_to_queue('sh', SHA, code_queue)
read_to_queue('sz', SZA, code_queue)


if __name__ == '__main__':
    print code_queue