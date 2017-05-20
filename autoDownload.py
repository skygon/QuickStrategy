import os
import sys
import urllib
import urllib2
import threading
import Queue

#==============================global variables==================================
# full url example : "http://market.finance.sina.com.cn/downxls.php?date=2017-05-18&symbol=sh603993"
base_url = "http://market.finance.sina.com.cn/downxls.php"
dest_dir = ".\detail_data"
SHA = ".\config\sh_a.txt"
SZA = '.\config\sz_a.txt'

thread_pool_num = 10
#code_file = ""

#download queue. Should be the all codes
download_queue = Queue.Queue()

#==================================End of global variables=========================


#===================Help functions==========================================
def usage():
    print '''
    usage:
    python autoDownload.py date_string
    example : python autoDownload.py "2017-05-18"
    '''

def read_to_queue(prefix, filename):
    f = open(filename)
    line = f.readline()
    while line:
        code = prefix + line.strip('\n')
        download_queue.put(code)
        line = f.readline()
    f.close()

def init_download_queue():
    # read codes from files
    read_to_queue('sh', SHA)
    read_to_queue('sz', SZA)

def compose_url(date_string, code):
    full_url = base_url + "?date=" + date_string + "&symbol=" + code
    return full_url

def mylogger(message, vars):
    print message %(vars)
#===================End of help functions 


class Worker(threading.Thread):
    def __init__(self, date_string):
        threading.Thread.__init__(self)
        self.date_string = date_string
        mylogger("date string is %s \n", self.date_string)
        self.start()
    
    def download(self, url, file_name):
        try:
            path = os.path.join(dest_dir, file_name)
            mylogger("save path is %s \n", path)
            urllib.urlretrieve(url, path)
        except Exception:
            print "ERROR: download from %s failed" %url

    def run(self):
        while True:
            try:
                #Immediate get one item or raise empty excepiton
                code = download_queue.get(False)
                mylogger( "I get code %s \n" , code )
                full_url = compose_url(self.date_string, code)
                mylogger( "full_url is %s \n" , full_url)
                file_name = code + ".csv"
                mylogger("filename is %s \n", file_name)
                self.download(full_url, file_name)
            except Queue.Empty:
                print "All code has been downloaded \n"
                #If queue is empty, we can exit worker thread now.
                break
            except Exception:
                #Ignore other exception. Just go to next download task
                print "ERROR: download failed \n"

def here_we_go(date_string):
    init_download_queue()
    threads = []
    for i in range(thread_pool_num):
        threads.append(Worker(date_string))
    
    for t in threads:
        if t.isAlive():
            t.join()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    
    date_string = sys.argv[1]
    here_we_go(date_string)
    print "I am main. And I am all"