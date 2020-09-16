files = ['data/raw/192.168.89.208/192.168.89.208_ms07-029.xml', 'data/raw/192.168.89.208/192.168.89.208_ms10-054.xml', 'data/raw/192.168.89.208/192.168.89.208_password.txt', 'data/raw/192.168.89.208/192.168.89.208_share.xml', 'data/raw/192.168.89.208/192.168.89.208_ms06-025.xml', 'data/raw/192.168.89.208/192.168.89.208_os.xml', 'data/raw/192.168.89.208/192.168.89.208_ms10-061.xml', 'data/raw/192.168.89.208/192.168.89.208_ms08-067.xml', 'data/raw/192.168.89.208/192.168.89.208_ms17-010.xml']
class filename:
    MS06 = "ms06-025.xml"
    MS07 = "ms07-029.xml"
    MS08 = "ms08-067.xml"
    MS10 = "ms10-054.xml"
    MS10_2 = "ms10-061.xml"
    MS17 = "ms17-010.xml"
    PSSWD = "password.txt"
    SHARE = "share.xml"
# for file in files:
#     if filename.MS06 in file:
#         print(file)
files.sort(key=None, reverse=False)
print(files)