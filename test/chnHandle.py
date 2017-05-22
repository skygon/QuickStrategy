# -*- coding: utf8 -*-
import os

#dest_dir = ".\detail_data"
#SHA = ".\config\sh_a.txt"
#SZA = '.\config\sz_a.txt'

BUY_STR = '\xe4\xb9\xb0\xe7\x9b\x98'
SELL_STR = '\xe5\x8d\x96\xe7\x9b\x98'

dest_dir = os.path.join(os.getcwd(), "detail_data")
SHA = os.path.join(os.getcwd(), "config", "sh_a.txt")
print SHA

s = '买盘'
ss = '卖盘'
print str(repr(s))
print repr(ss)

print repr(BUY_STR) == repr(s) # True
print repr(SELL_STR) == repr(ss) # True