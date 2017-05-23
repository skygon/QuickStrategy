import os

def enum(**enums):
    return type('Enum', (), enums)

DealType = enum(BUY = 1, SELL = 2, UNKNOW = 3)

#BUY_STR = '\xe4\xb9\xb0\xe7\x9b\x98'
#SELL_STR = '\xe5\x8d\x96\xe7\x9b\x98'

BUY_STR = '\xc2\xf2\xc5\xcc'
SELL_STR = '\xc2\xf4\xc5\xcc'
###========================================================================================###
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




if __name__ == '__main__':
    print DealType.BUY
    print DealType.SELL