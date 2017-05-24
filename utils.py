import os

def enum(**enums):
    return type('Enum', (), enums)

DealType = enum(BUY = 1, SELL = 2, UNKNOW = 3)

#BUY_STR = '\xe4\xb9\xb0\xe7\x9b\x98'
#SELL_STR = '\xe5\x8d\x96\xe7\x9b\x98'

BUY_STR = '\xc2\xf2\xc5\xcc'
SELL_STR = '\xc2\xf4\xc5\xcc'
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