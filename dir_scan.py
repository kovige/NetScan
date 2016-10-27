# -*- coding:utf8 -*-
import socket
import socks
import requests
import win_inet_pton
import threading
import Queue
import argparse
import sys
import ipaddress
import re
import time


class batch_scan(object):
    def __init__(self,ip_list):
        self.SOCKS_PROXY_HOST = '127.0.0.1'
        self.SOCKS_PROXY_PORT = 1234
        self.queue = Queue.Queue()
        self.dicPath = 'dic/'
        self.dic = []
        self.successList = []
        self.threads_num = 15
        self.header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'}
        self.scanlist = []
        self.ip_list = ip_list
        default_socket = socket.socket
        socks.set_default_proxy(socks.SOCKS5, self.SOCKS_PROXY_HOST,self.SOCKS_PROXY_PORT)
        socket.socket = socks.socksocket
    def choose_dic(self,dic_name):
        with open(self.dicPath+dic_name+'.txt' ,'rb') as dictionary :
            for line in dictionary.readlines() :
                line = line.strip()
                self.dic.append(line)
    def getList(self):
        for ip in self.ip_list:
            reqIp = ip
            print reqIp               
            try:
                res = requests.get(reqIp,headers = self.header,timeout = 5)
                headers = res.headers
                print headers
                powered_by = headers['x-powered-by'].lower()
                server = headers['server'].lower()
                if ('php') in powered_by:
                    self.choose_dic('php')
                elif ('asp') in powered_by:
                    self.choose_dic('asp')
                    self.choose_dic('aspx')
                elif ('jboss' and 'java' and 'jsp' and 'weblogic') in powered_by:
                    self.choose_dic('jsp')
                elif ('tomcat') in server:
                    self.choose_dic('jsp')
                elif ('centos' and 'linux' and 'redhat') in server:
                    self.choose_dic('php')
                    self.choose_dic('jsp')
                else:
                    pass                                 
            except Exception,e:
                print 'ip error'
                pass
            self.choose_dic('dir')
            self.choose_dic('backup')
            self.scanlist = []
            print len(self.dic)
            for dict in self.dic:
                scanUrl = ip+dict
                self.scanlist.append(scanUrl)
                self.queue.put(scanUrl)
            self.dic = []
    def scan(self):
        text404 = r'无法显示|信息提示|参数错误|no exists|User home page for|可疑输入拦截|D盾|安全狗|无法加载模块|[nN]ot [fF]ound|不存在|未找到|Error|Welcome to nginx!|404'
        reg404 = re.compile(text404)
        while True:
            if self.queue.empty():
                break
            try:
                target = self.queue.get_nowait()
                print target
                req  = requests.get(target,headers = self.header,timeout=5)
                try:
                    html = req.text.encode(req.encoding).decode('unicode_escape','ignore')
                except Exception,e:
                    html = req.text
                if req.status_code == 200 and not reg404.findall(html):
                    if '301' not in str(req.history):
                        print 'ok'
                        print target
                        self.successList.append(target)
                        
            except Exception,e:
                print e
                pass
            
        
    def run(self):
        threads = []
        for i in range(self.threads_num):
#         print str(i)
            t = threading.Thread(target=self.scan,name=str(i))
            threads.append(t)
 
        for t in threads:
            t.start()  
 
        for t in threads:
            t.join()
    
                

# class defined_scan(object):
#     def __init__(self,ip):
#         self.queue = Queue.Queue()
#         self.SOCKS_PROXY_HOST = '127.0.0.1'
#         self.SOCKS_PROXY_PORT = 1234
#         self.HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'}
#         self.ip_port = [22, 80, 443, 3389, 6379, 7001, 8080, 27017]
            
# list = []        
# with open('test.txt','rb') as dictionary:
#     for line in dictionary.readlines():
#         line = line.strip()
#         list.append(line)
#    
# test = batch_scan(list)
# test.getList()
# test.run()
# print test.successList
  