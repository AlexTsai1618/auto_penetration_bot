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
    vuln_count = {
        "cve_2020_1206":{"number":0,"ips":[]},
        "cve_2020_0796":{"number":0,"ips":[]},
        "ms07-029":{"number":0,"ips":[]},
        "ms08-067":{"number":0,"ips":[]},
        "ms10-054":{"number":0,"ips":[]},
        "ms10-061":{"number":0,"ips":[]},
        "ms17-010":{"number":0,"ips":[]},

    }
    for data in datas:
        file = open(data)
        data = json.load(file)
        ips.append(data['ip'])
        computer_os.append(data['os'])
        if data["cve_2020_1206"] == "Vulnerable":
            vuln_count["cve_2020_1206"]["number"] += 1
            vuln_count["cve_2020_1206"]["ips"].append(data['ip'])
        elif data["cve_2020_0796"] == "Vulnerable":
            vuln_count["cve_2020_0796"]["number"] += 1
            vuln_count["cve_2020_0796"]["ips"].append(data['ip'])
        elif data["ms07-029"] == "Vulnerable":
            vuln_count["ms07-029"]["number"] += 1
            vuln_count["ms07-029"]["ips"].append(data['ip'])
        elif data["ms08-067"] == "Vulnerable":
            vuln_count["ms08-067"]["number"] += 1
            vuln_count["ms08-067"]["ips"].append(data['ip'])
        elif data["ms10-054"] == "Vulnerable":
            vuln_count["ms10-054"]["number"] += 1
            vuln_count["ms10-054"]["ips"].append(data['ip'])
        elif data["ms10-061"] == "Vulnerable":
            vuln_count["ms10-061"]["number"] += 1
            vuln_count["ms10-061"]["ips"].append(data['ip'])
        elif data["ms17-010"] == "Vulnerable":
            vuln_count["ms17-010"]["number"] += 1
            vuln_count["ms17-010"]["ips"].append(data['ip'])                                                
    
    print(vuln_count)

def paths():
  
    path = os.path.join('data','clean_data')
    files = os.listdir(path)
    files = [os.path.join(path,file) for file in files]
    data_count(files)

if __name__ == "__main__":
    paths()
