import redis

'''
https://pypi.python.org/pypi/redis/2.10.5
'''

r = redis.Redis(host='localhost', port=6379, db=0)

r.hset('test_map', 'field1', 1)
r.hset('test_map', 'field2', 'hello')

data = r.hkeys('test_map')
print data

x = r.hget('test_map', 'field1')
print type(x)
print x