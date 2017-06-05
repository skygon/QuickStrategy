import redis
import json

class RedisOperator(object):
    def __init__(self, host, port, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.con = redis.Redis(host=self.host, port=self.port, db=self.db)

    #=====Emhancement operator functions=============#
    def hsetJson(self, table, field, value):
        s = json.dumps(value)
        self.con.hset(table, field, s)
    
    #==== redis command wrapper=======================#
    def hget(self, table, field):
        return self.con.hget(table, field)
    
    def hlen(self, table):
        return self.con.hlen(table)
    

    
