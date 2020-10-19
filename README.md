# SMB scanner
## Environment : python3.8
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
### 5. run RPC Backgroundly
```
$ msfrpcd -P yourpassword -S
```

### 6. run the program
```
python3 main.py
python3 report_generator.py
```

### 7. go to data/report get the report
```
cd data/report/<yourfile>

```