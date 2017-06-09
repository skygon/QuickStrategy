import json
import operator
from utils import *
from RedisOperator import RedisOperator

# get redis connection
r = RedisOperator('localhost',6379,0)
# sh small rank
sh_small = {} # code <-> changepercent

for k in code_vol_map['sh']['small'].keys():
    s = r.hget('index_4_dict', k)
    if s is None:
        continue
    data = json.loads(s)
    sh_small[k] = float(data['changepercent'])

ranked =  sorted(sh_small.items(), key=operator.itemgetter(1), reverse=True)
print ranked
