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
* asc: 是否升序
### return
```
(new String("158"))
```
说明5月26号这天，截止该API请求发出时，sh603993这支股票成交额大于20万的交易数有158笔。如果每页显示60条数据，则需要3页才能显示完。
## Get big deal list by amount
### API
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?symbol=sh603993&num=60&page=1&sort=ticktime&asc=0&volume=0&amount=200000&type=0&day=2017-05-26
### params
* amount: deal total amount, price * volume * 100
* day: string stands for date.
* num 每页显示的数据数目，这里为60
* page 页码号，从 1 开始， 结束页码为cell(count ／ 60). 更改page的参数值为2和3可以获取剩余的数据
### return
```
[
{symbol:"sh603993",name:"洛阳钼业",ticktime:"14:58:40",price:"4.230",volume:"182600",prev_price:"4.230",kind:"D"},{symbol:"sh603993",name:"洛阳钼业",ticktime:"14:58:29",price:"4.230",volume:"141100",prev_price:"4.230",kind:"U"},{symbol:"sh603993",name:"洛阳钼业",ticktime:"14:57:49",price:"4.220",volume:"234900",prev_price:"4.230",kind:"D"},
...
]
```
U: 买盘 D: 卖盘

## Get big deal summary
### API
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillSum?symbol=sh603993&num=60&sort=ticktime&asc=0&volume=0&amount=500000&type=0&day=2017-05-26
### params
amount 只能为50w, 100w, 200w, 500w, 1000w
### return
```
[{symbol:"sh603993",name:"洛阳钼业",opendate:"2017-05-26",minvol:"0",voltype:"13",totalvol:"6571003",totalvolpct:"0.169",totalamt:"27813787",totalamtpct:"0.169",avgprice:"4.233",kuvolume:"3019703",kuamount:"12791359",kevolume:"0",keamount:"0",kdvolume:"3551300",kdamount:"15022428",stockvol:"38797718",stockamt:"164474123"}]
```
* totalvol 该条件大单的成交量，单位：股
* totalvolpct 占当日成交量的比例
* totalamt 大单成交额，单位元
* avgprice 大单成交平均价格
* kuvolume 主买单
* kdvolumn 主卖单
* kevolume 中性
