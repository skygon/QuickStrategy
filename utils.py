import os

#===================================Global variables=========================
BUY_STR = '\xc2\xf2\xc5\xcc'
SELL_STR = '\xc2\xf4\xc5\xcc'


#===============================Big deal related=============================
BIG_DEAL = {}
# TODO volumn levels
BIG_DEAL['volumn'] = {}

# amount levels
BIG_DEAL['amount'] = {}
BIG_DEAL['amount'][0] = 30 * 10000
BIG_DEAL['amount'][1] = 60 * 10000
BIG_DEAL['amount'][2] = 100 * 10000
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


if __name__ == '__main__':
    print code_volumn