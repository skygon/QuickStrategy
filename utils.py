def enum(**enums):
    return type('Enum', (), enums)

DealType = enum(BUY = 1, SELL = 2, UNKNOW = 3)

#BUY_STR = '\xe4\xb9\xb0\xe7\x9b\x98'
#SELL_STR = '\xe5\x8d\x96\xe7\x9b\x98'

BUY_STR = '\xc2\xf2\xc5\xcc'
SELL_STR = '\xc2\xf4\xc5\xcc'

if __name__ == '__main__':
    print DealType.BUY
    print DealType.SELL