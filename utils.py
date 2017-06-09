import os
import Queue
import datetime

'''
Index 0 stand for "2017-06-05"
We will add a function to get a mapping between index and the date string
'''

#===================================Global variables=========================
BUY_STR = '\xc2\xf2\xc5\xcc'
SELL_STR = '\xc2\xf4\xc5\xcc'

SHA = os.path.join(os.getcwd(), "config", "sh_a.txt")
SZA = os.path.join(os.getcwd(), "config", "sz_a.txt")

DEFAULT_PAGE_SIZE = 60

#redis related
redis_conf = {}
redis_conf['name'] = {} # naming related configuration
redis_conf['name']['bill_list'] = 'detail'
redis_conf['name']['bill_list_summary'] = 'summary'
redis_conf['name']['stocks_index'] = 'index'

TABLE_DETAIL = "detail"
TABLE_SUMMARY = "summary"
INDEX = "index"


# special days since 2016-10-21
special_days = []
special_days.append(datetime.datetime.strptime('2017-01-02', '%Y-%m-%d'))
special_days.append(datetime.datetime.strptime('2017-01-27', '%Y-%m-%d'))
special_days.append(datetime.datetime.strptime('2017-02-01', '%Y-%m-%d'))
special_days.append(datetime.datetime.strptime('2017-02-02', '%Y-%m-%d'))
special_days.append(datetime.datetime.strptime('2017-04-04', '%Y-%m-%d'))
special_days.append(datetime.datetime.strptime('2017-05-01', '%Y-%m-%d'))
special_days.append(datetime.datetime.strptime('2017-05-29', '%Y-%m-%d'))
special_days.append(datetime.datetime.strptime('2017-05-30', '%Y-%m-%d'))
#TODO add more in 2017

# global queues
code_queue = Queue.Queue()
code_vol_map = {}

code_vol_map['sh'] = {}
code_vol_map['sh']['small'] = {}
code_vol_map['sh']['mid'] = {}
code_vol_map['sh']['big'] = {}

code_vol_map['sz'] = {}
code_vol_map['sz']['small'] = {}
code_vol_map['sz']['mid'] = {}
code_vol_map['sz']['big'] = {}



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

#==========================read all code into queue========================================================
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



#=====================Get SH small code into queue================================================
volume_info = os.path.join(os.getcwd(), "config", "volume_info")
big_vol = 5 * 10000 * 10000
small_vol = 1 * 10000 * 10000

def handleVolume(prefix, code, volume):
    if volume < small_vol:
        code_vol_map[prefix]['small'][code] = volume
    elif volume < big_vol:
        code_vol_map[prefix]['mid'][code] = volume
    else:
        code_vol_map[prefix]['big'][code] = volume

def getCodeQueueByType():
    f = open(volume_info)
    line = f.readline()
    while line:
        code, volume = line.strip('\n').split(',')
        volume = int(volume)
        line = f.readline()
        if volume == 0:
            continue
        
        # currently, we only interested at sh6xxx and sz000xxx. Not consider sz002xxx and sz300xxx
        if code.find("sh6") >= 0:
            prefix = "sh"
        elif code.find("sz000") >= 0:
            prefix = "sz"
        else:
            continue
        
        handleVolume(prefix, code, volume)
        
    f.close()

getCodeQueueByType()


if __name__ == '__main__':
    #print code_queue
    getCodeQueueByType()
    print "========sh=================="
    print len(code_vol_map['sh']['small'].keys())
    print len(code_vol_map['sh']['mid'].keys())
    print len(code_vol_map['sh']['big'].keys())
    print "=========sz================="
    print len(code_vol_map['sz']['small'].keys())
    print len(code_vol_map['sz']['mid'].keys())
    print len(code_vol_map['sz']['big'].keys())