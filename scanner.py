import masscan,json,subprocess,asyncio,threading

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

    def enum4liunx(self,ip):
        try:
            result = subprocess.check_output(['enum4linux','-a',ip],stderr=subprocess.STDOUT)
            result = result.decode('utf-8')
            print(ip + " in enum4linux!!!  "+ result)
        except subprocess.CalledProcessError as e:
            # raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
            result =e.output.decode('utf-8')
            print(ip + " in enum4linux!!!  "+ result)
    def nmap(self,ip):
        # subprocess.run(['enum4linux','-a',ip])
        print(ip+" in nmap!!!")

    async def smb_445_enumeration(self,ip):
        threads = []

        self.enum4liunx(ip)
        self.nmap(ip)
        # task1 = threading.Thread(target = enum4liunx,args=(ip))
        # task1.start()
        # threads.append(task1)
        # task2 = threading.Thread(target = nmap,args=(ip))
        # task2.start()
        # threads.append(task2)
        # for thread in threads:
        #     thread.join()
        return "success"
    async def smb_139_enumeration(self,ip):
 
        return "success"



SMB_scanner('192.168.89.1/24')