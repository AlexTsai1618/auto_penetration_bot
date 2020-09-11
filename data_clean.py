import xmltodict,os,threading

def report_generate():

def schedual(files):
    
    os_data = os_clean(files[0])
    account_data = account_clean(files[1])
    share_data = share_clean(files[2])
    datas = {
        "os_data":os_data,
        "account_data":account_data,
        "share_data":share_data
        "vuln_data":vuln_data
    }
def data_path():
    directories = os.listdir('data/raw')
    thread_list = []
    for directory in directories:
        temp_path = os.path.join('data/raw',directory)
        temp_files = os.listdir(temp_path)
        files = [temp_path+file for file in temp_files]
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
    with open(raw_file,'w')as file:
        os = parsed_file['nmaprun']['host']['hostscript']["script"]['elem'][0]['#text']
        fqdn = parsed_file['nmaprun']['host']['hostscript']["script"]['elem'][4]['#text']
        workgroup = parsed_file['nmaprun']['host']['hostscript']["script"]['elem'][6]['#text']
    return os,fqdn,workgroup
def account_clean(raw_file):
    with open(raw_file,'w') as file:
        raw = file.read()
        clean_data = raw[50::].split(' ')
        account = clean_data[0]
        password = clean1[2]
    return account,password