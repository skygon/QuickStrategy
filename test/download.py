import os
import urllib
import urllib2  
              
path = "E:\mywork\QuickStrategy\data"   
path =os.path.join(path,"data.xls")   

def downLoadPicFromURL(path,URL):  
    try:  
        urllib.urlretrieve(url , path) 
    except:  
        print '\tError retrieving the URL:', path  

url = "http://market.finance.sina.com.cn/downxls.php?date=2017-05-18&symbol=sh603993"
downLoadPicFromURL(path,url) 