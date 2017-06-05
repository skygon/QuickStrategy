import datetime

'''
2016.10.21 - 2016.12.31 : No special day
2017.01.01 - 2017.06.04 : 
2017-01-02
2017-01-27
2017-02-01
2017-02-02
2017-04-04
2017-05-01
2017-05-29
2017-05-30
'''

special_days = []
special_days.append(datetime.datetime.strptime('2017-01-02', '%Y-%m-%d'))
special_days.append(datetime.datetime.strptime('2017-01-27', '%Y-%m-%d'))
special_days.append(datetime.datetime.strptime('2017-02-01', '%Y-%m-%d'))
special_days.append(datetime.datetime.strptime('2017-02-02', '%Y-%m-%d'))
special_days.append(datetime.datetime.strptime('2017-04-04', '%Y-%m-%d'))
special_days.append(datetime.datetime.strptime('2017-05-01', '%Y-%m-%d'))
special_days.append(datetime.datetime.strptime('2017-05-29', '%Y-%m-%d'))
special_days.append(datetime.datetime.strptime('2017-05-30', '%Y-%m-%d'))

'''
s = "2017-06-04" 

t = datetime.datetime.strptime(s, '%Y-%m-%d')
print t.weekday()
t1 = t + datetime.timedelta(days = 1)
print t1.weekday()
'''


s1 = "2017-04-03"
spe_t = datetime.datetime.strptime("2017-02-02", '%Y-%m-%d')

t = datetime.datetime.strptime(s1, '%Y-%m-%d')
t1 = t + datetime.timedelta(days = 1)

if t1 in special_days:
    print "skip ", t1



