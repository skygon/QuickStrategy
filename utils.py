def enum(**enums):
    return type('Enum', (), enums)

DealType = enum(BUY = 1, SELL = 2)

BUY_STR = '\xe4\xb9\xb0\xe7\x9b\x98'
SELL_STR = '\xe5\x8d\x96\xe7\x9b\x98'

if __name__ == '__main__':
    print DealType.BUY
    print DealType.SELL