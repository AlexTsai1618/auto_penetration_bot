import masscan,json,subprocess,asyncio,threading,nmap,re,os
import json
from queue import Queue
import time
from subprocess import Popen,PIPE
import xml.etree.ElementTree as ET
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[91m'
    FAIL = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def port_scanning(i):
    print(bcolors.WARNING + bcolors.BOLD +"[+] We are now in port_scanning" + bcolors.ENDC)
    """
    This function is used to scan through smb portocol by port 139,445
    """
    tasks = list()
    nm = nmap.PortScanner()
    data = nm.scan(i,'445,139')

    ips = []
    for ip in data['scan']:
        
        if data["scan"][ip]["tcp"][445]["state"] == "open" or data["scan"][ip]["tcp"][139]["state"] == "open":
            
            
            print(bcolors.WARNING + bcolors.BOLD +"[+]"+ ip +" is founded" + bcolors.ENDC)
            path = 'data/raw/'+ip

            if not os.path.isdir(path):
                print(bcolors.OKGREEN + bcolors.BOLD +"[+]"+ ip +" folder is created" + bcolors.ENDC)
                os.mkdir('data/raw/'+ip)

            ips.append(i)

            task = threading.Thread(target=enum4liunx_ng_execute, args=(ip,))
            task.start()
            tasks.append(task)
        else:
            print(bcolors.FAIL + bcolors.BOLD +"[+] SMB was not detected in "+ip + bcolors.ENDC)
    for task in tasks:
        task.join()   


    
def enum4liunx_ng_execute(ip):
    print(bcolors.WARNING +"[+]" + ip +" is in enum4liunx!"+ bcolors.ENDC)

    subprocess.run(["python3","enum4linux-ng/enum4linux-ng.py","-As",ip,"-oJ","data/raw2/"+ip+".e4raw.json"],stdout=open(os.devnull,'wb'))
    return ip +" En4liunx Success!" 

if __name__ == "__main__":
    port_scanning("192.168.121.1/24")