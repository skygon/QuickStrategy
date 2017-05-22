def enum(**enums):
    return type('Enum', (), enums)

DealType = enum(BUY = 1, SELL = 2)



if __name__ == '__main__':
    print DealType.BUY
    print DealType.SELL