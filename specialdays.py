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