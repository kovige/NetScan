import socket
import socks
import requests
import win_inet_pton
import threading
import Queue
import argparse
import sys
import ipaddress
from dir_scan import batch_scan
import time

success_list = []
queue = Queue.Queue()
threads_num=15
             
def scan():
    SOCKS_PROXY_HOST = '127.0.0.1'
    SOCKS_PROXY_PORT = 1234
    HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'}
    ip_port = [22, 80, 443, 3389, 6379, 7001, 8080, 27017]


    default_socket = socket.socket
    socks.set_default_proxy(socks.SOCKS5, SOCKS_PROXY_HOST,SOCKS_PROXY_PORT)
    socket.socket = socks.socksocket
    while True:
        if queue.empty():
            break
        reqIp = queue.get_nowait()
        for port in ip_port:
            reqUrl = 'http://'+str(reqIp)+':'+str(port)
            print 'scanning '+reqUrl
            try:
                res = requests.get(reqUrl,headers=HEADER,timeout=5)
                html = res.text 
            except Exception,e:
                print 'get html error'
                continue
            if html:
                print 'ok'
                success_list.append(reqUrl)
                
                
         
             
def run():
    threads = []
    for i in range(threads_num):
#         print str(i)
        t = threading.Thread(target=scan,name=str(i))
        threads.append(t)
 
    for t in threads:
        t.start()  
 
    t.join()
    time.sleep(threads_num/2)

def parse_args():
    parser = argparse.ArgumentParser(description="A tool to scan local network")
    parser.add_argument('--ip', metavar='IP', type=str, default='', help='ip addresses like 192.168.1.1/24')
    if len(sys.argv) < 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    _check_args(args)
    return args


def _check_args(args):
    if not args.ip:
        msg = 'Use --ip to set the ip address'
        raise Exception(msg)


def ip_parse(ip):
    if str(ip).startswith('http'):
        ip = ip.replace('http://','')
    _ips = ip.strip()
    ips = ipaddress.IPv4Network(u'%s' % _ips, strict=False)
    return ips

def saveFile(data,save_path):
    f_obj = open(save_path, 'a')
    f_obj.write(data+'\n')
    f_obj.close()

if __name__ == '__main__':
    args = parse_args()
    ip_lists = ip_parse(args.ip)
    save_path = str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))+'_'+str(ip_lists[0])+'_ip.txt'
    for ip in ip_lists:
        queue.put(ip)
    run()
    for ip in success_list:
        saveFile(ip, save_path)
    batchScan = batch_scan(success_list)
    batchScan.getList()
    batchScan.run()
    dirScan_path = str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))+'_'+str(ip_lists[0])+'_dir.txt'
    for url in batchScan.successList:
        saveFile(url,dirScan_path)
    print 'finished.....'
        
    