# Redis Approach
As a first step, we can store all data into redis.
Windows installation of redis can be found here:
https://github.com/MSOpenTech/redis/releases

## Data Structure
Since data is stored in redis, in dict structure. It's very handy to add new attributes in to a dict structure.
### Current day's stock data
```python
stocks = {}
stocks[code] = {}
stocks[code]['init_price'] = xxx
# For real time strategy, current_price is indeed current price. When used for whold day analysis, current_price is the end price
stocks[code]['current_price'] = xxx 
stocks[code]['current_volume'] = xxx # Same usage as current_price
```
### Big Deal
```python
# Two types of big deal data
# First, total amount. Has five levels
big_deal_amount = {}
big_deal_amount[0] = {}
big_deal_amount[1] = {}
big_deal_amount[2] = {}
big_deal_amount[3] = {}
big_deal_amount[4] = {}

# Each level has the following attributes:
big_deal_amount[level]['time'] = []
big_deal_amount[level]['price'] = []
big_deal_amount[level]['volume'] = []
big_deal_amount[level]['type'] = []
```

