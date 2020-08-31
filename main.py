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

        nm = nmap.PortScanner()
        data = nm.scan(ipaddress,'445,139')

        
        for i in data['scan']:
        
            if data["scan"][i]["tcp"][445]["state"] == "open" or data["scan"][i]["tcp"][445]["state"] == "open":
                result = loop.run_until_complete(self.(i))
                t = threading.Thread(target=self.schedual, args=(i,))
                t.start()
                t.join()                
                # print(str(i)+" enumeration is "+ str(result))
    
    async def nmap(self,ip):
        
        return ip +" nmap Success!
    async def enum4liunx_ng_execute(self,ip):
        subprocess.run(["python3","./enum4linux-ng/enum4linux-ng.py","-As",ip,"-u"," ","-oJ","./report/"+ip+"/"+ip+".e4raw.json"])
        return ip +" En4liunx Success!"

    def schedual(self,ip):
    # def enum4liunx_ng(self):
        loop = asyncio.new_event_loop()
        task = [
            asyncio.ensure_future(self.enum4liunx_ng_execute(ip))
            asyncio.ensure_future(self.nmap(ip))
        ]
        # print(ip)
        # t = threading.Thread(target=self.enum4liunx_ng_execute, args=(ip,))
        # t.start()
        # t.join()
        # t2 = threading.Thread(target=self.nmap,args=(ip,))
        loop.run_until_complete(self.(i))

    async def ms

if __name__ == "__main__":
    Enum2Report("192.168.1.1/24")