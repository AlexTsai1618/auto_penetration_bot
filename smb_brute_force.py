import socket
from smb.SMBConnection import SMBConnection
 
ip = '192.168.89.214'
 
name = socket.gethostbyaddr(ip)
ipGet = socket.gethostbyname(name[0])
print(name, ipGet, sep='\n')
 
 
remote_name = name[0]
conn = SMBConnection('username', 'password', 'any_name', remote_name)
assert conn.connect(ip, timeout=3)
 
for s in conn.listShares():
    print('------------------------------------')
    print('name', s.name)
    print('comments', s.comments)
    print('isSpecial', s.isSpecial)
    print('isTemporary', s.isTemporary)
    
    ''' 
    SharedDevice.DISK_TREE      0x00
    SharedDevice.PRINT_QUEUE    0x01
    SharedDevice.COMM_DEVICE    0x02
    SharedDevice.IPC            0x03
    '''
    print('type', s.type)
    print('')
    print('### FileList ###')
    try:
        for f in conn.listPath(s.name, '/'):
            print(f.filename)
        
        for f in conn.listPath(s.name, '/game'):
            print(f.filename)
    except:
        print('### can not access the resource')
    print('------------------------------------')
    print('')
 
conn.close()
