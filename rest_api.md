# Real time deal details
## host ip
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php
## Get big deal list count by amount
### API
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillListCount?symbol=sh600900&num=60&page=1&sort=ticktime&asc=0&volume=0&amount=500000&type=0&day=2017-05-26
### params
### return
```
(new String("198"))
```

## Get big deal list by amount
### API
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillListCount?symbol=sh600900&num=60&page=1&sort=ticktime&asc=0&volume=0&amount=2000000&type=0&day=2017-05-26
### params
* amount: deal total amount, price * volume * 100
* day: string stands for date.
### return
