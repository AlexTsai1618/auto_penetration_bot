import masscan,json,subprocess,asyncio,threading,nmap,re,os
import json
from queue import Queue
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Enum2Report:

    def __init__(self,ipaddress):
        print(bcolors.OKBLUE +
        "\n _____                       ____  ____                       _  "+ 
        "\n| ____|_ __  _   _ _ __ ___ |___ \|  _ \ ___ _ __   ___  _ __| |_   "+ 
        "\n|  _| | '_ \| | | | '_ ` _ \  __) | |_) / _ \ '_ \ / _ \| '__| __|  "+ 
        "\n| |___| | | | |_| | | | | | |/ __/|  _ <  __/ |_) | (_) | |  | |_   "+ 
        "\n|_____|_| |_|\__,_|_| |_| |_|_____|_| \_\___| .__/ \___/|_|   \__|  "+ 
        "\n                                            |_|                   " + bcolors.ENDC
        )

        self.port_scanning(ipaddress)
        print(bcolors.WARNING +"[+]init"+ bcolors.ENDC)        
    def port_scanning(self,i):
        print(bcolors.WARNING +"[+]port_scanning"+ bcolors.ENDC)
        """
        This function is used to scan through smb portocol by port 139,445
        """
        tasks = list()
        nm = nmap.PortScanner()
        data = nm.scan(i,'445,139')

        ips = []
        for i in data['scan']:
        
            if data["scan"][i]["tcp"][445]["state"] == "open" or data["scan"][i]["tcp"][445]["state"] == "open":
                print("i")
                os.mkdir('data/raw/'+i)
                ips.append(i)
        # for i in ips:
            
                task = threading.Thread(target=self.schedual, args=(i,))
                task.start()
                tasks.append(task)

        for task in tasks:
            task.join()                
                # print(str(i)+" enumeration is "+ str(result))
    def nmap_run_script(self,ip,script,name):
        subprocess.run(['nmap','-p','445',ip,'--script',script,'-oX','data/raw/'+ ip +'/'+ ip +'_'+name+'.xml'])
    def nmap_enum(self,ip):
        print(bcolors.WARNING +"[+]" + ip +" is in nmap_enumartion!"+ bcolors.ENDC)
        nm=nmap.PortScanner()
        data = {"os_data":"","shares_data":""}
        if nm.scan(ip, '445',arguments='--script smb-os-discovery.nse')['scan'][ip]['hostscript']:
            self.nmap_run_script(ip,'smb-os-discovery.nse',"os")
            if nm.scan(ip,'445',arguments='--script nmap_script/scripts/smb-enum-shares.nse')['scan'][ip]['hostscript']:
                self.nmap_run_script(ip,'smb-enum-shares.nse',"share")
                # if nm.scan(ip,'445',arguments='--script nmap_script/scripts/smb-vuln*')['scan'][ip]['hostscript']:
                self.nmap_run_script(ip,'smb-vuln*',"vuln")               
        else:
            subprocess.run(['nmap','-p','445',ip,'-O','-v','-oX','data/raw/'+ ip +'/'+ ip +'_os.xml'])
            if nm.scan(ip,'445',arguments='--script nmap_script/scripts/smb-enum-shares.nse')['scan'][ip]['hostscript']:
                self.nmap_run_script(ip,'smb-enum-shares.nse',"share")
                # if nm.scan(ip,'445',arguments='--script nmap_script/scripts/smb-vuln*')['scan'][ip]['hostscript']:
                self.nmap_run_script(ip,'smb-vuln*',"vuln") 
        # data['shares_data'] = nm.scan(ip,'445',arguments='--script nmap_script/scripts/smb-enum-shares.nse')['scan'][ip]['hostscript'][0]['output']
        # path = 'data/raw/'+ip+'/nmap_enum.json'
        # with open(path,'w') as file:
        #     json.dump(data,file)  

   

    
    def smb_brute_force(self,ip):
        print(bcolors.WARNING +"[+]" + ip +" is in brute_force!"+ bcolors.ENDC)
        try:
            subprocess.run(['medusa','-M','smbnt','-h',ip,'-u','admin','-P','data/wordlist/dummypass.txt','-f','-O','data/raw/'+ip+'/'+ip+'_password.txt'])
        except subprocess.CalledProcessError as e:
            raise BuildError('\'%s\' exited with error code: %s' % (name, e.returncode))
            file_path = 'data/raw/'+ip+'/'+ip+'_password.txt'
            file = open(file_path,'w')
            file.write("password is strong!!")
            file.close()
        return ip +" Brute Force Success!"  
           
    def schedual(self,ip):

        # t1 = threading.Thread(target=self.enum4liunx_ng_execute, args=(ip,))
        t2 = threading.Thread(target=self.nmap_enum, args=(ip,))
        t3 = threading.Thread(target=self.smb_brute_force, args=(ip,))
        
        # t1.start()
        t2.start()
        t3.start()

        # t1.join()
        t2.join()
        t3.join()

def enum4liunx_ng_execute(ip):
    print(bcolors.WARNING +"[+]" + ip +" is in enum4liunx!"+ bcolors.ENDC)
    subprocess.run(["python3","enum4linux-ng/enum4linux-ng.py","-As",ip,"-u"," ","-oJ","data/raw/"+ip+"/"+ip+".e4raw.json"])
    return ip +" En4liunx Success!" 
if __name__ == "__main__":
    # enum4liunx_ng_execute("192.168.89.208")
    Enum2Report("192.168.89.208")






     #subprocess.run(['nmap','-p','445',"192.168.89.208",'--script','smb-enum-shares.nse','-oX','data/raw/'+ "192.168.89.208" +'/'+  +'192.168.89.208_share.xml'])
