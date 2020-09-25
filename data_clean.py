import xmltodict,os,threading,subprocess,json


# def report_generate(datas):
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[91m'
    FAIL = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class filename:
    MS06 = "ms06-025.xml"
    MS07 = "ms07-029.xml"
    MS08 = "ms08-067.xml"
    MS10 = "ms10-054.xml"
    MS10_2 = "ms10-061.xml"
    MS17 = "ms17-010.txt"
    PSSWD = "password.txt"
    SHARE = "share.xml"
    OS = "os.xml"
    CVE2020 = "cve_2020_1206.txt"
    CVE2020_2 = "cve_2020_0796.txt"
def checkfile(files,filename_end,modelname):
    try:
    
        if modelname == "nmap_datas":
            data =  nmap_datas([e for e in files if e.endswith(filename_end)][0])
            return data
        elif modelname == "os_clean":
            os_data,fqdn,workgroup =  os_clean([e for e in files if e.endswith(filename_end)][0])

            return os_data,fqdn,workgroup
        elif modelname == "share_clean":
            data = share_clean([e for e in files if e.endswith(filename_end)][0])
            return data
        elif modelname == "handle_txt_file":
            data = handle_txt_file([e for e in files if e.endswith(filename_end)][0])
            return data
        elif modelname == "account_clean":
            account,password = account_clean([e for e in files if e.endswith(filename_end)][0])
            return account,password
    except:

        if modelname == "nmap_datas":
            return "NULL"
        elif modelname == "os_clean":
            return "NULL","NULL","NULL"
        elif modelname == "share_clean":
            return "NULL"
        elif modelname == "handle_txt_file":
            return "NULL"
        elif modelname == "account_clean":
            return "NULL","NULL"
def schedual(filepath,files,ip):
    # if ip == "192.168.121.173":
    import os
    all_files = os.listdir(filepath)
    os_data,fqdn,workgroup = checkfile(files,filename.OS,"os_clean")
    # os_data,fqdn,workgroup = os_clean([e for e in files if e.endswith(filename.OS)][0])
    
    account,password = checkfile(files,filename.PSSWD,"account_clean")
    share_data = checkfile(files,filename.SHARE,"share_clean")
    ms07029_data = checkfile(files,filename.MS07,"nmap_datas")
    ms08067_data = checkfile(files,filename.MS08,"nmap_datas")
    ms10054_data = checkfile(files,filename.MS10,"nmap_datas")
    ms10061_data = checkfile(files,filename.MS10_2,"nmap_datas")
    ms17010_data = checkfile(files,filename.MS17,"handle_txt_file")
    # cve_2020_0796_data = handle_txt_file([e for e in files if e.endswith(filename.CVE2020)][0])
    cve_2020_0796_data = checkfile(files,filename.CVE2020,"handle_txt_file")
    # cve_2020_1206_data = handle_txt_file([e for e in files if e.endswith(filename.CVE2020_2)][0])
    cve_2020_1206_data = checkfile(files,filename.CVE2020_2,"handle_txt_file")
    datas = {
        "ip":ip,
        "os":os_data,
        "fqdn":fqdn,
        "workgroup":workgroup,
        "account":account,
        "password":password,
        "share_data":share_data,
        "cve_2020_1206":cve_2020_1206_data,
        "cve_2020_0796":cve_2020_0796_data,
        "ms07-029":ms07029_data,
        "ms08-067":ms08067_data,
        "ms10-054":ms10054_data,
        "ms10-061":ms10061_data,
        "ms17-010":ms17010_data,

    }
    datas = json.dumps(datas)
    outputfile = ip + ".json"
    print(datas) 
    filepath = 'data/clean_data/'+outputfile
    print(bcolors.OKBLUE + bcolors.BOLD +"[+] " + ip + " json file is generated"  + bcolors.ENDC)
    with open(filepath,'w')as file:
        file.write(datas)
def nmap_datas(raw_files):
    
    with open(raw_files,"rb")as file:
        parsed_file = xmltodict.parse(file)
        if "hostscript" not in parsed_file['nmaprun']['host']:
            message =  "Not Vulernable"
            return message  
        else:
            if "#text" not in parsed_file['nmaprun']['host']['hostscript']["script"]:
                if parsed_file['nmaprun']['host']['hostscript']["script"]["@output"] == "ERROR: Script execution failed (use -d to debug)":
                    message = "Not Vulnerable"
                    return message  
                elif parsed_file['nmaprun']['host']['hostscript']["script"]["table"]["elem"][1]["#text"] == "VULNERABLE" :
                    message =  "Vulnerable"
                    return message  
            else:
                if parsed_file['nmaprun']['host']['hostscript']["script"]["#text"] == "false":
                    message = "Not Vulnerable"    
                    return message  
    
    
        
    
def handle_txt_file(raw_files):
    try:
        with open(raw_files,'r')as file:
            result = file.read()
            print(result)
            if result == "Vulnerable" or "vulnerable":
                return "Vulnerable"
            else:
                return "Not Vulnerable"
    except:
        return "Not Vulnerable"
    
def data_path():
    directories = os.listdir('data/raw_data')
    thread_list = []
    for directory in directories:
        temp_path = os.path.join('data/raw_data',directory)
        temp_files = os.listdir(temp_path)
        files = [os.path.join(temp_path,file) for file in temp_files]
        task = threading.Thread(target=schedual, args=(temp_path,files,directory))
        task.start()
        thread_list.append(task)
    for thread in thread_list:
        thread.join()
def share_clean(raw_file):
    with open(raw_file,"rb") as raw_file:
        try:
            parsed_file = xmltodict.parse(raw_file)
            data = {}
            tables =  parsed_file['nmaprun']['host']['hostscript']["script"]['table']
            temp = []
            for i in tables:
                temp.append(i['elem'][2]["@key"])
                temp.append(i['elem'][2]["#text"])
                temp.append(i['elem'][3]["@key"])
                temp.append(i['elem'][3]["#text"])
                data[i["@key"]] = temp
                temp = []
            return data
        except:
            data = "NULL"
            return data
def os_clean(raw_file):
    data = {}
    import os
    if os.path.isfile(raw_file):
        with open(raw_file,'rb')as file:
            parsed_file = xmltodict.parse(file)
            try:
                parsed_file2 = parsed_file['nmaprun']['host']
                os_info = parsed_file2[0]['#text']
                fqdn = parsed_file2[4]['#text']
                workgroup = parsed_file2[6]['#text']
                print("here A")
                return os_info,fqdn,workgroup
            except:

                try:
                    parsed_file2 = parsed_file['nmaprun']['host']["os"]['osmatch'][0]['@name']
                    os_info = parsed_file2
                    return os_info,"NULL","NULL"
                except:
                    return "NULL","NULL","NULL"
def account_clean(raw_file):
    if os.path.isfile(raw_file):
        with open(raw_file,'r') as file:
            try:
                raw = [file for file in file.readlines() if file.startswith("ACCOUNT FOUND:")][0]
                clean_data = raw[51::].split(' ')
                account = clean_data[0]
                password = clean_data[2]
                return account,password
            except:
                return "NULL","NULL"
    else:
        return "NULL","NULL"
if __name__ == "__main__":
    data_path()
