

def report_generate():

def data_collection():

def share_clean(raw_file):
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
def password_clean(raw_file):
    with open(raw_file,'w') as file:
        raw = file.read()
        clean_data = raw[50::].split(' ')
        account = clean_data[0]
        password = clean1[2]
    return account,password