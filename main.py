import masscan,json,subprocess,asyncio,threading,nmap,re
from queue import Queue
import time
class Enum2Report:
    def __init__(self,ipaddress):
    
        print(
        "\n _____                       ____  ____                       _  "+ 
        "\n| ____|_ __  _   _ _ __ ___ |___ \|  _ \ ___ _ __   ___  _ __| |_   "+ 
        "\n|  _| | '_ \| | | | '_ ` _ \  __) | |_) / _ \ '_ \ / _ \| '__| __|  "+ 
        "\n| |___| | | | |_| | | | | | |/ __/|  _ <  __/ |_) | (_) | |  | |_   "+ 
        "\n|_____|_| |_|\__,_|_| |_| |_|_____|_| \_\___| .__/ \___/|_|   \__|  "+ 
        "\n                                            |_|                   " 
        )

        self.port_scanning(ipaddress)

    def port_scanning(self,ipaddress):

        """
        This function is used to scan through smb portocol by port 139,445
        """

        mas = masscan.PortScanner()
        mas.scan(ipaddress, ports='445,139')
        data = mas.scan_result
        loop = asyncio.new_event_loop()
        
        for ip in data['scan']:
            print(data['scan'][ip])
        
            if data['scan'][ip]['tcp'][139]['state']=="open" or data['scan'][ip]['tcp'][445]['state']=="open":
                result = loop.run_until_complete(self.enum4liunx_ng_schedual(ip))
                print(str(ip)+" port 139 enumeration "+ str(result))

    def enum4liunx_ng_execute(self,ip):
        subprocess.run(["python3","./enum4linux-ng/enum4linux-ng.py","-As",ip,"-u"," ","-oJ","./report/"+ip+".e4raw.json"])
        return ip +" En4liunx Success!"

    async def enum4liunx_ng_schedual(self,ip):
    # def enum4liunx_ng(self):
        print(ip)
        t = threading.Thread(target=self.enum4liunx_ng_execute, args=(ip,))
        t.start()
        t.join()
        # print(ip)
        # try:
        #     result = subprocess.check_output(['enum4linux','-a',ip],stderr=subprocess.STDOUT)
        #     result = result.decode('utf-8')
        #     print(ip + " in enum4linux!!!  "+ result)
        # except subprocess.CalledProcessError as e:
        #     # raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        #     result = e.output.decode('utf-8')
  

if __name__ == "__main__":
    Enum2Report("192.168.88.208")