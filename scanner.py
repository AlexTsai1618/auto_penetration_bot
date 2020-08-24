import masscan,json,subprocess,asyncio,threading,nmap

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
        This function is used to scan through smb portocol by port 139,445
        """

        ips_445 = []
        ips_139 = []
        ips_137 = []
        ips_138 = []
        mas = masscan.PortScanner()
        mas.scan(ipaddress, ports='445,139,137,138', arguments='--max-rate 1000')
        data = mas.scan_result
        loop = asyncio.new_event_loop()
        
        for ip in data['scan']:
            print(data['scan'][ip])
            # if data['scan'][ip]['udp'][137]['state']=="open":
            #     result = loop.run_until_complete(self.smb_137_enumeration(ip))
            #     print(ip+" port 137 enumeration "+result)
            #     ips_137.append(ip)
            # if data['scan'][ip]['udp'][138]['state']=="open":
            #     result = loop.run_until_complete(self.smb_138_enumeration(ip))
            #     print(ip+" port 138 enumeration "+result)
            #     ips_138.append(ip)
            
            if data['scan'][ip]['tcp'][139]['state']=="open":
                result = loop.run_until_complete(self.smb_139_enumeration(ip))
                print(ip+" port 139 enumeration "+result)
                ips_139.append(ip)
            if data['scan'][ip]['tcp'][445]['state']=="open":
                result = loop.run_until_complete(self.smb_445_enumeration(ip))
                print(ip+" port 445 enumeration "+result)
                ips_445.append(ip)

    def enum4liunx(self,ip):
        print(ip)
        try:
            result = subprocess.check_output(['enum4linux','-a',ip],stderr=subprocess.STDOUT)
            result = result.decode('utf-8')
            print(ip + " in enum4linux!!!  "+ result)
        except subprocess.CalledProcessError as e:
            # raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
            result = e.output.decode('utf-8')
            print(ip + " in enum4linux!!!  "+ result)
    def nmap_445_os_discovery(self,ip):
        nm = nmap.PortScanner()
        data = nm.scan(ip, '445', arguments='--script=./nmap_script/scripts/smb-os-discovery.nse')
        with open('./report/'+ip+"txt",'W') as file:
            file.write(data)
        print(data)
        print(ip+" in nmap_445_os_discovery!!!")
    def nmap_445_enum_shares(self,ip):
        nm = nmap.PortScanner()
        data = nm.scan(ip, '445', arguments='--script=./nmap_script/scripts/smb-enum-shares.nse')
        print(data)
        print(ip+" in nmap_445_os_discovery!!!")
    # def nmap_445(self,ip):
    #     async nmap_
    #     print(ip+" in nmap!!!")
    # def nmap_445(self,ip):
    #     async nmap_
    #     print(ip+" in nmap!!!")
    
    async def smb_445_enumeration(self,ip):
        threads = []

        # self.enum4liunx(ip)
        # self.nmap(ip)
        print(ip)
        task1 = threading.Thread(target = self.enum4liunx,args=(ip,))
        task1.start()
        task1.join()
        task2 = threading.Thread(target = self.nmap_445_os_discovery,args=(ip,))
        task2.start()
        task2.join()
        # threads.append(task2)
        # for thread in threads:
        #     thread.join()
        return "success"

    async def smb_137_enumeration(self,ip):
 
        return "success"

    async def smb_138_enumeration(self,ip):
 
        return "success"

    async def smb_139_enumeration(self,ip):
 
        return "success"



SMB_scanner('192.168.89.1/24')