import os
import re
import numpy as np
from docx.shared import Mm
from docxtpl import DocxTemplate, RichText,InlineImage
import json
from datetime import date
import matplotlib.pyplot as plt
from data_poc import poc_module
import nmap
import matplotlib.pyplot as plt2

# names = ('SMB x '+ str(data["ips"]),'RDP x '+ str(len(self.ip)),)
# size = [data["ips"],len(self.ip)]
# print(size,names)
# color_codes = ['#FF2D01','#FAA40E']
# my_circle=plt.Circle( (0,0), 0.7, color='white')
# plt2.pie(size, labels=names, colors=color_codes)
# p2=plt2.gcf()
# p2.gca().add_artist(my_circle)
# plt2.savefig('data/picture/pic0.jpg', format='jpg',dpi = 1000)
def port_scanning(ip):
        
    """
    This function is used to scan through smb portocol by port 139,445
    """
    tasks = list()
    nm = nmap.PortScanner()
    data = nm.scan(ip,'3389')

    ips = []
    for ip in data['scan']:
        
        if data["scan"][ip]["tcp"][3389]["state"] == "open" :
            ips.append(ip)
    return ips
if __name__ == "__main__":
    result1 = port_scanning("10.6.51.1/24")
    result2 = port_scanning("10.6.6.1/24")
    print("resutl1")
    for ip in result1:
        print(ip)
    print("result2")
    for ip2 in result2:
        print(ip2)
