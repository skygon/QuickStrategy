# Real time deal details
## GUI Address
http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill.php?symbol=sh603993
## Get big deal list count by amount
### API
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillListCount?symbol=sh603993&num=60&page=1&sort=ticktime&asc=0&volume=0&amount=200000&type=0&day=2017-05-26
### params
* symbol: code
* sort: ticktime - 逐笔； 应该还有一个分时的，但是要收费。
* amount: 总额
* day: date string.
### return
```
(new String("158"))
```

## Get big deal list by amount
### API
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?symbol=sh603993&num=60&page=1&sort=ticktime&asc=0&volume=0&amount=200000&type=0&day=2017-05-26
### params
* amount: deal total amount, price * volume * 100
* day: string stands for date.
* num 每页显示的数据数目
* page 页码号，从 1 开始， 结束页码为cell(count ／ 60)
* 
### return
