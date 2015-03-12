# -*- coding: utf-8 -*-

"""
    data_download.py
    ~~~~~~~~~~~~

    Download data from DataYes Mercury.

    :copyright: (c) 2015 by DataYes Fixed Income Team.
    :Author: taotao.li
    :last updated: Mar.10th.2014
"""

"""
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
"""

"""
Code Tips:
why use:
print u"Want to download file {} [1-yes/0-no]: ".format(filename),
download_this = input()
other than:
download_this = input(u"Want to download file {} [1-yes/0-no]: ".format(filename))

because: method 2 will show a :UnicodeEncodeError: 'ascii' codec can't encode characters in position 22-33: ordinal not in range(128): when
filename is unicode encoded, so strange, need more deep understanding. But in Ipython, everything is ok.
"""


import sys
import os
import ConfigParser
import requests


DEBUG = False
AUTHORIZE_URL = "https://gw.wmcloud.com/usermaster/authenticate.json"
MERCURY_URL = 'https://gw.wmcloud.com/mercury/api/databooks'
DOWNLOAD_URL = 'https://gw.wmcloud.com/mercury/databooks'


def parse_args(argv):
	if DEBUG:
		for i in argv:
			print i
	# user file
	if '-f' in argv:
		index = argv.index('-f') + 1
		filename = argv[index] if index < len(argv) else ""
		if not filename:
			return False
		if filename not in os.listdir('.'):
			return False
	elif '-u' not in argv or '-p' not in argv:
		return False
	else:
		try:
			argv[argv.index('-u') + 1]
			argv[argv.index('-p') + 1]
		except:
			return False	

	return True

def get_user_password(argv):
	if '-f' in argv:
		cf = ConfigParser.ConfigParser()
		cf.read(argv[argv.index('-f') + 1])
		user = cf.get('userpwd', 'user')
		pwd = cf.get('userpwd', 'pwd')
	else:
		user = argv[argv.index('-u') + 1]
		pwd = argv[argv.index('-p') + 1]

	return user, pwd

def authorize_user(user, pwd):
	url = AUTHORIZE_URL
	user, tenant = user.split("@")
	data = dict(username=user, password=pwd, tenant=tenant)
	res = requests.post(url, data)
	if not res.ok or not res.json().get('content', {}).get('accountId', 0):
		return False, None
	else:
		cookie = res.json().get('content', {}).get('token', {}).get('tokenString', '')
		return True, cookie

def list_data(cookies):
	url = MERCURY_URL
	res = requests.get(url, cookies=cookies)
	if not res.ok:
		print 'Request error, maybe a server error, please retry or contact us directly'
		return 0
	data = res.json()
	print "Hello, Sir/Madam, there are {} files in your DataYes Mercury VM".format(str(len(data)))
	all_data = [i['name'] for i in data]
	for i in all_data:
		print u'Name: {}'.format(i)

	return all_data

def download_file(url, cookies, filename):
	dataurl = url + '/' + filename			
	print u'\nStart download {}'.format(filename),

	with open(filename, 'wb') as f:
	    response = requests.get(dataurl, cookies=cookies, stream=True)

	    if not response.ok:
	        print u'Something is wrong when download file {} '.format(filename)
	        return 0
	    
            for chunk in response.iter_content(1024 * 100):
		print '...',
	    	f.write(chunk)

def main():
	# import pdb;pdb.set_trace()
	argv = sys.argv
	user, pwd = "", ""
	ALL = False
	all_files = []
	if '-a' in argv:
		ALL = True
	elif '-d' in argv:
		index = argv.index('-d')
		for i in range(index+1, len(argv)):
			print argv[i]
			all_files.append(argv[i])
	else:
		pass

	# step 1: parse command line arguments
	if not parse_args(argv):
		print "USAGE: python data_download.py -f [filename] -u [username] -p [password] -a"
		print "the 'filename' above is the file contains your user and password as the format :"
		print "[userpwd]\nuser=username\npwd=password"
		return 0
	else:
		user, pwd = get_user_password(argv)

	# step 2: validate user
	legal, cookie = authorize_user(user, pwd)
	if not legal:
		print "username are password are not validate"
		return 0

	# step 3: check mercury data list
	cookies = {'cloud-sso-token': cookie}
	all_data = list_data(cookies)

	# step 4: download mercury data one by one
	print '\nHello, Sir/Madam, are you ready, let\'s see how the amazing things happen here ...'
	url = DOWNLOAD_URL
	if ALL:
		for i in all_data:
			download_file(url, cookies, i)
	elif all_files:
		for i in all_files:
			if i in all_data:
				download_file(url, cookies, i)
			else:
				print u'Sorry, there does not exist file {} in your DataYes Mercury'.format(i)
				continue
	else:
		pass


if __name__ == '__main__':
	main()
