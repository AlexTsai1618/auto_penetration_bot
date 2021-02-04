# SMB scanner
## Environment : kali liunx
## Programming language : Python3.8
![Alt Text](smb_tool.gif)
### 0. setup environment
```
sudo apt update
sudo apt install python3-pip 
```
### 1. download this project
```
git clone https://github.com/alexboy60318/smb_scanner.git
```
### 2. install pipenv library
```
pip install pipenv
```
### 3. Using pipenv to install all the libraies you need
```
cd smb_scanner
pipenv install
```
### 4. After finishing the installation activate the virtual env
```
pipenv shell
```
If you successfully activate the enviroment,it would be like this.
```
(smb_scanner) root@kali:/home/kali/Desktop/smb_scanner#
```
### 6. run the program
#### go to main.py line 242 type the ip range
#### go to data_poc.py line 30 renew your host ip

```
python3 main.py
```

### 7. get the report
```
ex: 20201213/result.html
[date]/result.html
```
### 8. Download report
```
ex: scp -r 20201213 root@192.168.168.23:/
scp -r date_folder remote_account@remote_ip:path
```