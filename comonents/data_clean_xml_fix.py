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

def checkfile(all_files,filename_end,modelname):
    if filename_end in all_files:
        if modelname == "nmap_datas":
            data =  nmap_datas([e for e in files if e.endswith(filename_end)][0])
            return data
        elif modelname == "os_clean":
            os,fqdn,workgroup =  os_clean([e for e in files if e.endswith(filename_end)][0])
            return os_data,fqdn,workgroup
        elif modelname == "share_clean":
            data = share_clean([e for e in files if e.endswith(filename_end)][0])
            return data
        
    else:
        if modelname == "nmap_datas":
            return "NULL"
        elif modelname == "os_clean":
            return "NULL","NULL","NULL"
        elif modelname == "share_clean":
            return "NULL"
     
def schedual(files,ip):
    all_files = os.listdir(files)
    
   
    os_data,fqdn,workgroup = checkfile(all_files,filename.OS,"os_clean")
    share_data = checkfile(all_files,filename.SHARE,"share_clean")
    account,password = account_clean([e for e in files if e.endswith(filename.PSSWD)][0])
    ms07029_data = checkfile(all_files,filename.MS07,"nmap_datas")
    ms08067_data = checkfile(all_files,filename.MS07,"nmap_datas")
    ms10054_data = checkfile(all_files,filename.MS07,"nmap_datas")
    ms10061_data = checkfile(all_files,filename.MS07,"nmap_datas")
    ms17010_data = handle_txt_file([e for e in files if e.endswith(filename.MS17)][0])
    cve_2020_0796_data = handle_txt_file([e for e in files if e.endswith(filename.CVE2020)][0])
    cve_2020_1206_data = handle_txt_file([e for e in files if e.endswith(filename.CVE2020_2)][0])
    share_data = share_clean([e for e in files if e.endswith(filename.SHARE)][0])


    # ms08067_data = nmap_datas([e for e in files if e.endswith(filename.MS08)][0])

    # ms10054_data = nmap_datas([e for e in files if e.endswith(filename.MS10)][0])

    # ms10061_data = nmap_datas([e for e in files if e.endswith(filename.MS10_2)][0])

    # ms17010_data = handle_txt_file([e for e in files if e.endswith(filename.MS17)][0])

    # cve_2020_0796_data = handle_txt_file([e for e in files if e.endswith(filename.CVE2020)][0])
    # cve_2020_1206_data = handle_txt_file([e for e in files if e.endswith(filename.CVE2020_2)][0])
    datas = {
        "ip":ip,
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
    # datas = json.dumps(datas)
    # outputfile = ip + ".json"
    
    # filepath = 'data/clean_data/'+outputfile
    # print(bcolors.OKBLUE + bcolors.BOLD +"[+] " + ip + " json file is generated"  + bcolors.ENDC)
    # with open(filepath,'w')as file:
    #     file.write(datas)



schedual("data/raw/192.168.121.5","192.168.121.11")