import masscan,json,subprocess,asyncio,threading,nmap,re,os
import json
from queue import Queue
import time
class Enum2Report:

    def main(self,ipaddress):
        print(
        "\n _____                       ____  ____                       _  "+ 
        "\n| ____|_ __  _   _ _ __ ___ |___ \|  _ \ ___ _ __   ___  _ __| |_   "+ 
        "\n|  _| | '_ \| | | | '_ ` _ \  __) | |_) / _ \ '_ \ / _ \| '__| __|  "+ 
        "\n| |___| | | | |_| | | | | | |/ __/|  _ <  __/ |_) | (_) | |  | |_   "+ 
        "\n|_____|_| |_|\__,_|_| |_| |_|_____|_| \_\___| .__/ \___/|_|   \__|  "+ 
        "\n                                            |_|                   " 
        )

        self.port_scanning(ipaddress)
        print("init")        
    def port_scanning(self,i):
        print("port_scanning")
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
    
    def nmap_enum(self,ip):
        print("[+]" + ip +" is in nmap_enumartion!")
        nm=nmap.PortScanner()
        data = {"os_data":"","shares_data":""}
        if nm.scan(ip, '445',arguments='--script smb-os-discovery.nse')['scan'][ip]['hostscript']:
            data['os_data'] = nm.scan(ip, '445',arguments='--script nmap_script/scripts/smb-os-discovery.nse')['scan'][ip]['hostscript'][0]['output']
            if nm.scan(ip,'445',arguments='--script nmap_script/scripts/smb-enum-shares.nse')['scan'][ip]['hostscript']:
                data['shares_data'] = nm.scan(ip,'445',arguments='--script nmap_script/scripts/smb-enum-shares.nse')['scan'][ip]['hostscript'][0]['output']
            else:
                data['shares_data'] = 'NULL'
        else:
            data['os_data'] = np.scan("192.168.88.1",arguments='-O -v')['scan']['192.168.88.1']['osmatch'][0]['name']
            if nm.scan(ip,'445',arguments='--script nmap_script/scripts/smb-enum-shares.nse')['scan'][ip]['hostscript']:
                data['shares_data'] = nm.scan(ip,'445',arguments='--script nmap_script/scripts/smb-enum-shares.nse')['scan'][ip]['hostscript'][0]['output']
            else:
                data['shares_data'] = 'NULL'
        # data['shares_data'] = nm.scan(ip,'445',arguments='--script nmap_script/scripts/smb-enum-shares.nse')['scan'][ip]['hostscript'][0]['output']
        path = 'data/raw/'+ip+'/nmap_enum.json'
        with open(path,'w') as file:
            json.dump(data,file)  

   
    def enum4liunx_ng_execute(self,ip):
        print("[+]" + ip +" is in enum4liunx!")
        subprocess.run(["python3","./enum4linux-ng/enum4linux-ng.py","-As",ip,"-u"," ","-oJ","data/raw/"+ip+"/"+ip+".e4raw.json"])
        return ip +" En4liunx Success!"      

    
    def smb_brute_force(self,ip):
        print("[+]" + ip +" is in brute_force!")
        try:
            subprocess.run(['medusa','-M','smbnt','-h',ip,'-u','admin','-P','data/wordlist/passlist.txt','-f','-O','data/raw/'+ip+'/'+ip+'_password.txt'])
        except subprocess.CalledProcessError as e:
            raise BuildError('\'%s\' exited with error code: %s' % (name, e.returncode))
            file_path = 'data/raw/'+ip+'/'+ip+'_password.txt'
            file = open(file_path,'w')
            file.write("password is strong!!")
            file.close()
        return ip +" Brute Force Success!"  
           
    def schedual(self,ip):

        t1 = threading.Thread(target=self.enum4liunx_ng_execute, args=(ip,))
        t2 = threading.Thread(target=self.nmap_enum, args=(ip,))
        t3 = threading.Thread(target=self.smb_brute_force, args=(ip,))
        
        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()


if __name__ == "__main__":
    Enum2Report().smb_brute_force("192.168.88.1")