import os
# from docxtpl import DocxTemplate
import json
def report(datas):
    return 0
def data_count(datas):
    ips = []
    computer_os = []
    os_count = {
        "Windows 10":0,
        "Windows 7":0,
        "Windows 8":0,
        "Windows XP":0,
        "Windows Server 2016":0,
        "Windows Server 2012 R2":0,
        "Windows Server 2008 R2":0,
        "Windows Server 2008":0
    }
    for data in datas:
        file = open(data)
        data = json.load(file)
        ips.append(data['ip'])
        computer_os.append(data['os'])
    
    print(len(ips),computer_os)

def paths():
  
    path = os.path.join('data','clean_data')
    files = os.listdir(path)
    files = [os.path.join(path,file) for file in files]
    data_count(files)

if __name__ == "__main__":
    paths()
