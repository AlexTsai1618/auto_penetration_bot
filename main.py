import json,subprocess,asyncio,threading,nmap,re,os
import json
from queue import Queue
import time
from subprocess import Popen,PIPE
import xml.etree.ElementTree as ET
# class paths:
    
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[91m'
    FAIL = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Enum2Report:

    def __init__(self,ipaddress):
        print(bcolors.OKBLUE + bcolors.BOLD + 
        """        
        ███████╗███╗   ██╗██╗   ██╗███╗   ███╗██████╗ ██████╗ ███████╗██████╗  ██████╗ ██████╗ ████████╗
        ██╔════╝████╗  ██║██║   ██║████╗ ████║╚════██╗██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝
        █████╗  ██╔██╗ ██║██║   ██║██╔████╔██║ █████╔╝██████╔╝█████╗  ██████╔╝██║   ██║██████╔╝   ██║   
        ██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══██╗██╔══╝  ██╔═══╝ ██║   ██║██╔══██╗   ██║   
        ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║███████╗██║  ██║███████╗██║     ╚██████╔╝██║  ██║   ██║   
        ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
        """                                                                                                      
         + bcolors.ENDC
        )
        
        self.port_scanning(ipaddress)
        print(bcolors.OKBLUE + bcolors.BOLD +"[+] We are now in port_scanning" + bcolors.ENDC)
    def port_scanning(self,i):
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
                path = 'data/raw_data/'+ip

                if not os.path.isdir(path):
                    print(bcolors.OKGREEN + bcolors.BOLD +"[+]"+ ip +" folder is created" + bcolors.ENDC)
                    os.mkdir('data/raw_data/'+ip)

                ips.append(i)

                task = threading.Thread(target=self.schedule, args=(ip,))
                task.start()
                tasks.append(task)
            else:
                print(bcolors.FAIL + bcolors.BOLD +"[+] SMB was not detected in "+ip + bcolors.ENDC)
        for task in tasks:
            task.join()                
    
    def nmap_run_script(self,ip,script,name):
        print(bcolors.WARNING + bcolors.BOLD +"[+] "+ip+" "+ name + " exploit has started" + bcolors.ENDC)
        
        try:
            subprocess.run(['nmap','-p','445',ip,'--script',script,'-oX','data/raw_data/'+ ip +'/'+ ip +'_'+name+'.xml'],stdout=open(os.devnull,'wb'))
        except:
            filename = 'data/raw_data/'+ ip +'/'+ ip +'_'+name+'.txt'
            with open(filename,'wb')as file:
                file.write("NULL")
        print(bcolors.OKGREEN + bcolors.BOLD + "[+] "+ip+" "+ name + " exploit has Finished" + bcolors.ENDC)
    def nmap_enum(self,ip):
        print(bcolors.WARNING + bcolors.BOLD + "[+]" + ip +" is in nmap_enumartion!" + bcolors.ENDC)
        nm=nmap.PortScanner()
        # data = {"os_data":"","shares_data":""}
        if 'hostscript' in nm.scan(ip,arguments='--script smb-os-discovery.nse')['scan'][ip]:
            # self.nmap_run_script(ip,'smb-os-discovery.nse',"os")
        #     if nm.scan(ip,'445',arguments='--script nmap_script/scripts/smb-enum-shares.nse')['scan'][ip]['hostscript']:
            t0 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-os-discovery.nse',"os",))
            # t1 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-vuln-ms06-025',"ms06-025",))
            # t2 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-vuln-ms07-029',"ms07-029",))
            t3 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-vuln-ms08-067',"ms08-067",))
            # t4 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-vuln-ms10-054',"ms10-054",))
            # t5 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-vuln-ms10-061',"ms10-061",))
            t6 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-enum-shares.nse',"share",))
            t7 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-vuln-ms17-010',"ms17-010",))
            t0.start()
            # t1.start()
            # t2.start()
            t3.start()
            # t4.start()
            # t5.start()
            t6.start()
            t7.start()
            t0.join()
            # t1.join()
            # t2.join()
            t3.join()
            # t4.join()
            # t5.join()
            t6.join()
            t7.join()        
        else:
            subprocess.run(['nmap','445',ip,'-O','-oX','data/raw_data/'+ ip +'/'+ ip +'_os.xml'])
            t1 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-vuln-ms06-025',"ms06-025",))
            t2 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-vuln-ms07-029',"ms07-029",))
            t3 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-vuln-ms08-067',"ms08-067",))
            t4 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-vuln-ms10-054',"ms10-054",))
            t5 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-vuln-ms10-061',"ms10-061",))
            t6 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-enum-shares.nse',"share",))
            t7 = threading.Thread(target=self.nmap_run_script, args=(ip,'smb-vuln-ms17-010',"ms17-010",))
            # t1.start()
            # t2.start()
            t3.start()
            # t4.start()
            # t5.start()
            t6.start()
            t7.start()
            # t1.join()
            # t2.join()
            t3.join()
            # t4.join()
            # t5.join()
            t6.join()
            t7.join()

        print(bcolors.OKGREEN + bcolors.BOLD + "[+] " + ip +" has finished nmap_enumartion!"+ bcolors.ENDC)
    
    def smb_brute_force(self,ip):
        print(bcolors.WARNING + bcolors.BOLD + "[+] " + ip +" is in brute_force!"+ bcolors.ENDC)
        path = 'data/raw_data/'+ip+'/'+ip+'_password.txt'
        try:
            subprocess.run(['medusa','-M','smbnt','-h',ip,'-U','data/wordlist_data/dummyusernames.txt','admin','-P','data/wordlist_data/dummypass.txt','-f','-O','data/raw_data/'+ip+'/'+ip+'_password.txt'],stdout=open(os.devnull,'wb'))
            self.check_file(path)
        except:
            file = open(path,'w')
            file.write("password is strong!!")
            file.close()
            self.check_file(path)
        print(bcolors.OKGREEN + bcolors.BOLD + "[+] " + ip +" brute_force has finished!"+ bcolors.ENDC)  
           
    def schedule(self,ip):

       
        t1 = threading.Thread(target=self.smbghost_detection, args=(ip,))
        t2 = threading.Thread(target=self.nmap_enum, args=(ip,))
        t3 = threading.Thread(target=self.smb_brute_force, args=(ip,))
        
        t5 = threading.Thread(target=self.smb_bleeding_detection,args=(ip,))

        
        t1.start()
        t2.start()
        t3.start()

        t5.start()
        t1.join()
        t2.join()
        t3.join()

        t5.join()
    def ms17_010_detection(self,ip):
        print(bcolors.WARNING + bcolors.BOLD + "[+] " + ip +" ms17_010_detection is going!"+ bcolors.ENDC)
        filename = ip + "_ms17-010.txt"
        path = "data/raw_data/" + ip + '/' + filename
        try:
            subprocess.run(['python2','ms17-010.py','-i',ip],stdout=open(os.devnull,'wb'))
            self.check_file(path)
        except:
            self.check_file(path)
        print(bcolors.OKGREEN + bcolors.BOLD + "[+] " + ip +" ms17_010_detection have just finished!"+ bcolors.ENDC)  
    def smb_bleeding_detection(self,ip):
        print(bcolors.WARNING + bcolors.BOLD + "[+] " + ip +" smb_bleeding_detection is going!"+ bcolors.ENDC)
        filename = ip + "_cve_2020_1206.txt"
        path = "data/raw_data/" + ip + '/' + filename
        try:
            subprocess.run(['python3','SMBleed-detection/SMBGhost-SMBleed-scanner.py',ip],stdout=open(os.devnull,'wb'))
            self.check_file(path)
            print(bcolors.OKGREEN + bcolors.BOLD + "[+] " + ip +" smb_bleeding_detection have just finished!"+ bcolors.ENDC)  
        except:

            file2 = open(path,"w")
            file2.write("Not vulnerable")
            file2.close()
            self.check_file(path)
            print(bcolors.OKGREEN + bcolors.BOLD + "[+] " + ip +" smb_bleeding_detection have just finished!"+ bcolors.ENDC)  
    def smbghost_detection(self,ip):
        print(bcolors.WARNING + bcolors.BOLD +"[+]" + ip +" is in smbghost detection"+ bcolors.ENDC)
        import socket
        import struct
        import sys
        from netaddr import IPNetwork
        sock = socket.socket(socket.AF_INET)
        sock.settimeout(3)
        pkt = b'\x00\x00\x00\xc0\xfeSMB@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$\x00\x08\x00\x01\x00\x00\x00\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00x\x00\x00\x00\x02\x00\x00\x00\x02\x02\x10\x02"\x02$\x02\x00\x03\x02\x03\x10\x03\x11\x03\x00\x00\x00\x00\x01\x00&\x00\x00\x00\x00\x00\x01\x00 \x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\n\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
        try:
            sock.connect(( str(ip),  445 ))
        except:
            sock.close()
            

        sock.send(pkt)

        nb, = struct.unpack(">I", sock.recv(4))
        res = sock.recv(nb)
        filename = ip + "_cve_2020_0796.txt"
        path = "data/raw_data/" + ip + '/' + filename
        if res[68:70] != b"\x11\x03" or res[70:72] != b"\x02\x00":

            print(path)
            with open(path,'w')as file:
                file.write("Not vulnerable")
                self.check_file(path)    
                print(bcolors.OKGREEN + bcolors.BOLD + "[+] " + ip +" smbghost detection has finished!"+ bcolors.ENDC)
        else:
            with open(path,'w')as file:
                file.write("vulnerable")            

                self.check_file(path)    
                print(bcolors.OKGREEN + bcolors.BOLD + "[+] " + ip +" smbghost detection has finished!"+ bcolors.ENDC)
    def check_file(self,path):
        path = os.path.join(path)
        if not os.path.isfile(path):
            with open(path,'w')as file:
                file.write("NULL")
            print(bcolors.OKGREEN + bcolors.BOLD + "[+] " + path +" has been checked and fixed!"+ bcolors.ENDC)
        else:
            print(bcolors.OKGREEN + bcolors.BOLD + "[+] " + path +" is greate nothing need to do!"+ bcolors.ENDC)
                      
def enum4liunx_ng_execute(ip):
    print(bcolors.WARNING +"[+]" + ip +" is in enum4liunx!"+ bcolors.ENDC)
    subprocess.run(["python3","enum4linux-ng/enum4linux-ng.py","-As",ip,"-u"," ","-oJ","data/raw_data/"+ip+"/"+ip+".e4raw_data.json"],stdout=open(os.devnull,'wb'))
    return ip +" En4liunx Success!" 

if __name__ == "__main__":
    Enum2Report("192.168.110.0/24")
    subprocess.run(['python3','data_clean.py'])
    subprocess.run(['python3','report_generator.py'])
    #10.