# Redis
As a first step, we can store all data into redis.
Windows installation of redis can be found here:
https://github.com/MSOpenTech/redis/releases

## Data Structure
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
