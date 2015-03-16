# mercury-client


# Tutorial


## 1. Install python 2.7                                                                                                         

## 2. Install mercury-client package from Github

   Datayes Official Github is: https://github.com/DataYes/mercury-client, You can download the mercury-client package here.
   Or download directly from [here](http://litaotao.github.io/files/mercuryclient.rar)

### 2.1 Uncompress the package
### 2.2 Intall the package
    
- Open the command line tool 
    - windows: cmd
    - linux/mac: terminal
- Use the ***cd*** command to go the the package directory which contains ***setup.py*** file 
- Execute command ***python setup.py install*** to install the mercury-client package

## 3. USAGE:

***Steps***

- Get an client instance
    - import mercury
    - client = mercury.Client(username='username', password='password')
- Use that instance to list/get/delete your files in Datayes Mercury.
    - lists()
        Show the all the data in one user's mercury data zone.
    - get(filename='', download_all=False)
        Get user's data according to filename, can be a string or a list of string. 
        If set all to True, will download all the data file. 
    - delete(filename)
        Delete user's data according to filename, can only be a string.

***EXAMPLES***

    import mercury
    client = mercury.Client('taotao.li@datayes.com', 'password')
    all_files = client.lists()
    client.get(filename='123.txt')
    client.delete(filename='123.txt')

Bellow is the screenshot of the above:
![mercury-client.jpg](http://litaotao.github.io/images/mercury-client.jpg)

# 中文使用步骤
    
- 安装Python 2.7
- 安装mercury-client包
- 生成client实例
- 使用client进行list/get/delete操作



