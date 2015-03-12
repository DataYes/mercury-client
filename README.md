# mercury-client


# Tutorial

## 1. Preparation [option]

To download your data, you need to be authorized. So please provide a file contains your full username and password or just provide your username and password as command arguments.

If you set your username and password in a file, make sure the format of the file is as follows:

    [userpwd]
    user=username
    pwd=password

## 2. Ready to Download Data

### 2.1 Install python 2.7                                                                                                         

### 2.2 Install requests lib
    After installing python successfully, user can use pip to install lots of userful third python libraries, to download data from web, 
    you need to install requests lib first.
    Here is the command : pip install requests

### 2.3 USAGE:

***NAME***

data_download - download user's data file in DataYes Mercury

***SYNOPSIS***

python data_download.py [OPTION]

***DESCRIPTION***

Download user's data file in DataYes Mercury, need provide username and password to validate user.

    -f [filename]

        the 'filename' above is the file contains your user and password as the format :
        [userpwd]\nuser=username\npwd=password

    -u [username]
        username

    -p [password]
        password

    -a 
        download all the data files.

    -d 
        download specified files.
        ps: If use this parameter to choose specified files to download, make sure the filename only contains ASCII code.

***EXAMPLES***

    python data_download.py -f userpwd.txt -a

    python data_download.py -u username -p password -a

    python data_download.py -u username -p password -d 123.txt factors.xls

# 中文使用步骤
    
- 安装Python 2.7
- 安装Python第三方库requests
- 运行下载指令：
    + 提供用户名密码 [2选1，-f参数优先]
        * -f 用户名密码文件，有文件格式要求，必须是：
            [userpwd]
            user=username
            pwd=password
        * -u username -p password
    + 指定需要下载的文件 [2选1，-a参数优先]
        * -a：下载所有数据文件
        * -d 所需下载文件名：可以指定多个文件，此时不能输入中文文件名，如果用此方法，请确保输入文件名为英文；若需下载中文文件，可以使用-a参数；


