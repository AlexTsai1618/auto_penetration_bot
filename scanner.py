import masscan,json,subprocess,asyncio

class SMB_scanner:

    def __init__(self,ipaddress):

        print( "  _____ __  __ ____   _____" +                               
           "\n / ____|  \/  |  _ \ / ____|                                "+
           "\n| (___ | \  / | |_) | (___   ___ __ _ _ __  _ __   ___ _ __ "+
           "\n \___ \| |\/| |  _ < \___ \ / __/ _` | '_ \| '_ \ / _ \ '__| "+
           "\n ____) | |  | | |_) |____) | (_| (_| | | | | | | |  __/ | " +  
           "\n|_____/|_|  |_|____/|_____/ \___\__,_|_| |_|_| |_|\___|_| ")

        self.port_scanning(ipaddress)

    def port_scanning(self,ipaddress):

        """
        This function is used to scan throug smb port 139,445
        """

        ips_445 = []
        ips_139 = []
        mas = masscan.PortScanner()
        mas.scan(ipaddress, ports='445,139', arguments='--max-rate 1000')
        data = mas.scan_result
        loop = asyncio.new_event_loop()
        
        for ip in data['scan']:
            if data['scan'][ip]['tcp'][139]['state']=="open":
                result = loop.run_until_complete(self.smb_139_enumeration(ip))
                print(ip+" port 139 enumeration "+result)
                ips_139.append(ip)
            if data['scan'][ip]['tcp'][445]['state']=="open":
                result = loop.run_until_complete(self.smb_445_enumeration(ip))
                print(ip+" port 445 enumeration "+result)
                ips_445.append(ip)
        # self.nmap_smb_enumeration(ips_139,ips_445)
    
    async def smb_445_enumeration(self,ip):
    
        return "success"
    async def smb_139_enumeration(self,ip):
 
        return "success"



SMB_scanner('192.168.89.1/24')