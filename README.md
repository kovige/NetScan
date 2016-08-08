NetScan
===================

配合reGeorg使用的内网扫描工具

Requirements
------------
* Python 2.6+
* pysocks
* win_inet_pton（解决windows下pysocks报错）

Example
------------

**reGeorg：**
将tunnel.jsp 上传至目标机（http://xx.com）
本机：python reGeorgSocksProxy.py -p 1234 -u http://xx.com/tunnel.jsp

**net_scan:**
python net_scan.py --ip 192.168.10.0/24


Extra
-------
* 内网ip扫描+敏感路径扫描。敏感路径扫描自动根据返回包中powered_by和server选择字典，默认扫描目录和备份。当前字典文件为空，需自行添加，如果字典文件名改了，程序里面也要改。
* 如果只需要内网ip扫描，将程序（net_scan.py）最后几行注释：


    batchScan = batch_scan(success_list)
    batchScan.getList()
    batchScan.run()
    dirScan_path = str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))+'_'+str(ip_lists[0])+'_dir.txt'
    for url in batchScan.successList:
        saveFile(url,dirScan_path)
    print 'finished.....'

代码写得不好，只实现具体功能~