import masscan,json,subprocess,asyncio,threading,nmap,re,os
import json
from queue import Queue
import time
class Enum2Report:
    def __init__(self,ipaddress):
    
        print(
        "\n _____                       ____  ____                       _  "+ 
        "\n| ____|_ __  _   _ _ __ ___ |___ \|  _ \ ___ _ __   ___  _ __| |_   "+ 
        "\n|  _| | '_ \| | | | '_ ` _ \  __) | |_) / _ \ '_ \ / _ \| '__| __|  "+ 
        "\n| |___| | | | |_| | | | | | |/ __/|  _ <  __/ |_) | (_) | |  | |_   "+ 
        "\n|_____|_| |_|\__,_|_| |_| |_|_____|_| \_\___| .__/ \___/|_|   \__|  "+ 
        "\n                                            |_|                   " 
        )

        self.port_scanning(ipaddress)

    def port_scanning(self,i):

        """
        This function is used to scan through smb portocol by port 139,445
        """

        nm = nmap.PortScanner()
        data = nm.scan(i,'445,139')

        
        for i in data['scan']:
        
            if data["scan"][i]["tcp"][445]["state"] == "open" or data["scan"][i]["tcp"][445]["state"] == "open":
                os.mkdir('data/raw/'+i)
                t = threading.Thread(target=self.schedual, args=(i,))
                t.start()
                t.join()                
                # print(str(i)+" enumeration is "+ str(result))
    
    def nmap_enum(self,ip):
        nm=nmap.PortScanner()
        data = {"os_data":"","shares_data":""}
        data['os_data'] = nm.scan(ip, '445', arguments='./scripts/smb-os-discovery.nse')
        data['shares_data'] = nm.scan(ip,'445',arguments='./scripts/smb-enum-shares.nse')
        path = 'data/raw/'+ip+'/nmap_enum.json'
        with open(path,'w') as file:
            json.dump(data,file)  

   
    def enum4liunx_ng_execute(self,ip):
        # try:
        subprocess.run(["python3","./enum4linux-ng/enum4linux-ng.py","-As",ip,"-u"," ","-oJ","data/raw/"+ip+"/"+ip+".e4raw.json"])
        return ip +" En4liunx Success!"      

    
    def smb_brute_force(self,ip):
        
        subprocess.check_output(['medusa','-M','smbnt','-h',ip,'-U','data/wordlist/usernames.txt','-p','data/wordlist/passlist.txt','-F','-O','/'+ip+'/'+ip+'_password.txt'])
        return ip +" Brute Force Success!"  
           
    def schedual(self,ip):

        t1 = threading.Thread(target=self.enum4liunx_ng_execute, args=(ip,))
        t1.start()
        t1.join()
        t2 = threading.Thread(target=self.nmap_enum, args=(ip,))
        t2.start()
        t2.join()
        t3 = threading.Thread(target=self.smb_brute_force, args=(ip,))
        t3.start()
        t3.join()


if __name__ == "__main__":
    Enum2Report("192.168.1.106")