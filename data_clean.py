import xmltodict,os,threading

# def report_generate(datas):
class filename:
    MS06 = "ms06-025.xml"
    MS07 = "ms07-029.xml"
    MS08 = "ms08-067.xml"
    MS10 = "ms10-054.xml"
    MS10_2 = "ms10-061.xml"
    MS17 = "ms17-010.xml"
    PSSWD = "password.txt"
    SHARE = "share.xml"
    OS = "os.xml"

def schedual(files):

    files.sort(key=None, reverse=False)
    # print(files[0])
    print(files)

    os,fqdn,workgroup = os_clean([e for e in files if e.endswith(filename.OS)][0])
    account,password = account_clean([e for e in files if e.endswith(filename.PSSWD)][0])
    share_data = share_clean([e for e in files if e.endswith(filename.SHARE)][0])
    datas = {
        "os":os,
        "fqdn":fqdn,
        "workgroup":workgroup,
        "account":account,
        "password":password,
        "share_data":share_data,
        # "vuln_data":vuln_data
    }
    print(datas)
    print(os,fqdn,workgroup,account,password,share_data)
def nmap_datas(raw_files):
    raw_file = open(raw_file,"rb")
    parsed_file = xmltodict.parse((raw_file))
    
def data_path():
    directories = os.listdir('data/raw')
    thread_list = []
    for directory in directories:
        temp_path = os.path.join('data/raw',directory)
        # print(temp_path)
        temp_files = os.listdir(temp_path)
        # print(temp_files)
        files = [os.path.join(temp_path,file) for file in temp_files]
        # print(files)
        
        task = threading.Thread(target=schedual, args=(files,))
        task.start()
        thread_list.append(task)
    for thread in thread_list:
        thread.join()
def share_clean(raw_file):
    raw_file = open(raw_file,"rb")
    parsed_file = xmltodict.parse((raw_file))
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
def os_clean(raw_file):
    data = {}
    with open(raw_file,'rb')as file:
        parsed_file = xmltodict.parse((file))
        os = parsed_file['nmaprun']['host']['hostscript']["script"]['elem'][0]['#text']
        fqdn = parsed_file['nmaprun']['host']['hostscript']["script"]['elem'][4]['#text']
        workgroup = parsed_file['nmaprun']['host']['hostscript']["script"]['elem'][6]['#text']
    return os,fqdn,workgroup
def account_clean(raw_file):
    with open(raw_file,'r') as file:
        raw = file.read()
        print(raw)        
        clean_data = raw[50::].split(' ')
        account = clean_data[0]
        password = clean_data[1]
        
    return account,password
    
# print(account_clean('data/raw/192.168.89.208/192.168.89.208_password.txt'))
data_path()