import xmltodict,os,threading,subprocess

# def report_generate(datas):
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

def schedual(files):
    os,fqdn,workgroup = os_clean([e for e in files if e.endswith(filename.OS)][0])
    account,password = account_clean([e for e in files if e.endswith(filename.PSSWD)][0])
    share_data = share_clean([e for e in files if e.endswith(filename.SHARE)][0])
    ms07029_data = nmap_datas([e for e in files if e.endswith(filename.MS07)][0])
    ms08067_data = nmap_datas([e for e in files if e.endswith(filename.MS08)][0])
    ms10054_data = nmap_datas([e for e in files if e.endswith(filename.MS10)][0])
    ms10061_data = nmap_datas([e for e in files if e.endswith(filename.MS10_2)][0])
    ms17010_data = handle_txt_file([e for e in files if e.endswith(filename.MS17)][0])
    cve_2020_0796_data = handle_txt_file([e for e in files if e.endswith(filename.CVE2020)][0])
    cve_2020_1206_data = handle_txt_file([e for e in files if e.endswith(filename.CVE2020_2)][0])
    datas = {
        "os":os,
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
    print(datas)
    print(os,fqdn,workgroup,account,password,share_data)
def nmap_datas(raw_files):
    
    with open(raw_files,"rb")as file:
        parsed_file = xmltodict.parse(file)
        if "hostscript" not in parsed_file['nmaprun']['host']:
            message =  "Not Vulernable"
        else:
            if parsed_file['nmaprun']['host']['hostscript']["script"]["@output"] == "false" or parsed_file['nmaprun']['host']['hostscript']["script"]["@output"] == "ERROR: Script execution failed (use -d to debug)":
                message = "Not Vulnerable"
            else:
                message =  "Vulnerable"
    return message
def handle_txt_file(raw_files):
    with open(raw_files,'r')as file:
        result = file.read()
    return result
def data_path():
    directories = os.listdir('data/raw')
    thread_list = []
    for directory in directories:
        temp_path = os.path.join('data/raw',directory)
        temp_files = os.listdir(temp_path)
        files = [os.path.join(temp_path,file) for file in temp_files]
        task = threading.Thread(target=schedual, args=(files,))
        task.start()
        thread_list.append(task)
    for thread in thread_list:
        thread.join()
def share_clean(raw_file):
    with open(raw_file,"rb") as raw_file:
        parsed_file = xmltodict.parse(raw_file)
        try:
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
    with open(raw_file,'rb')as file:
        parsed_file = xmltodict.parse((file))
        parsed_file2 = parsed_file['nmaprun']['host']['hostscript']["script"]['elem']
        try:
            os = parsed_file2[0]['#text']
            fqdn = parsed_file2[4]['#text']
            workgroup = parsed_file2[6]['#text']
            return os,fqdn,workgroup
        except:
            return "NULL","NULL","NULL","NULL"
def account_clean(raw_file):
    with open(raw_file,'r') as file:
        try:
            raw = [file for file in file.readlines() if file.startswith("ACCOUNT FOUND:")][0]
            clean_data = raw[50::].split(' ')
            account = clean_data[0]
            password = clean_data[2]
            return account,password
        except:
            return "NULL","NULL"
if __name__ == "__main__":
    data_path()
