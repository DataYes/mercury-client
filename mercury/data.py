# -*- coding: utf-8 -*-

"""
    data.py
    ~~~~~~~~~~~~

    Download data from DataYes Mercury.

    :copyright: (c) 2015 by DataYes Fixed Income Team.
    :Author: taotao.li
    :last updated: Mar.10th.2014
"""

import sys
import os
import ConfigParser
import requests


DEBUG = False
AUTHORIZE_URL = "https://gw.wmcloud.com/usermaster/authenticate.json"
MERCURY_URL = 'https://gw.wmcloud.com/mercury/api/databooks'
DOWNLOAD_URL = 'https://gw.wmcloud.com/mercury/databooks'
NOTEBOOK_URL = 'https://gw.wmcloud.com/mercury/api/notebooks'
DOWNLOAD_NOTEBOOK_URL = 'https://gw.wmcloud.com/mercury/files'


class Client(object):
	"""DataYes Mercury Client

	Methods for the caller:

	- __init__(username, password)
		username and password here are which used by users to login www.datayes.com
	- lists()
		Show the all the data in one user's mercury data zone.
	- get(filename='', download_all=False)
		Get user's data according to filename, can be a string or a list of string. 
		If set all to True, will download all the data file. 
	- delete(filename)
		Delete user's data according to filename, can only be a string.
	"""
	def __init__(self, username, password, token=''):
		if DEBUG:
			import pdb; pdb.set_trace()
		if not token:
			self.username = username
			self.password = password
			print 'Welcome, {} ... '.format(username)
			self.isvalid, self.token = authorize_user(username, password)
			self.cookies = {'cloud-sso-token': self.token}
			if not self.isvalid:
				print 'Sorry, {}, your username or password are not match, authorization failed ...'.format(username)
		else:
			self.isvalid = True
			self.cookies = {'cloud-sso-token': token}

	def lists(self):
		'''
		Show the all the data in one user's mercury data zone.
		'''
		if not self.isvalid:
			print 'Sorry, {}, your username or password are not match, authorization failed ...'
			reutrn 
		self.all_data = list_data(self.cookies)
		self.all_notebook = list_notebook(self.cookies)
		

	def get(self, filename='', download_all=False):
		'''
		Get user's data according to filename, can be a string or a list of string. 
		If set all to True, will download all the data file. 
		'''
		if not self.isvalid:
			print 'Sorry, {}, your username or password are not match, authorization failed ...'
			reutrn 

		if download_all:
			self.lists()
			for i in self.all_data:
				download_file(self.cookies, i)
			return True
		elif type(filename) == list:
			for i in filename:
				download_file(self.cookies, i)
			return True
		elif type(filename) == str:
			download_file(self.cookies, filename)
			return True
		else:
			pass

		return False

	def notebook(self, filename='', download_all=True):
		'''
		Get user's notebook according to filename, can be a string or a list of string. 
		If set all to True, will download all the notebook file, just for back up.
		'''
		if not self.isvalid:
			print 'Sorry, {}, your username or password are not match, authorization failed ...'
			reutrn 

		if download_all:
			self.lists()
			for i in self.all_notebook:
				download_notebook(self.cookies, i)
			return True
		elif type(filename) == list:
			for i in filename:
				download_notebook(self.cookies, i)
			return True
		elif type(filename) == str:
			download_notebook(self.cookies, filename)
			return True
		else:
			pass

		return False

	def push(self, filepath):
		'''
		Push a file to your DataYes Mercury zone.
		'''
		try:
			files = {'datafile': open(filepath, 'rb')}
		except:
			print u"Can not open file at: ".format(filepath)
			return False

		r = requests.post(MERCURY_URL, files=files, cookies=self.cookies)

		print r.json().get('message', '') if not r.ok else ''

		return r.ok
		
	def delete(self, filename):
		'''
		Delete user's data according to filename, can only be a string.
		'''
		res = delete_file(self.cookies, filename)
		if res:
			print u'Delete file {} done ...'.format(filename)
		else:
			print u'Something is wrong when trying to delete file {} ...'.format(filename)


def authorize_user(user, pwd):
	url = AUTHORIZE_URL
	if '@' in user:
		user, tenant = user.split("@") 
	else:
		return False, None
	data = dict(username=user, password=pwd, tenant=tenant)
	res = requests.post(url, data)
	if not res.ok or not res.json().get('content', {}).get('accountId', 0):
		return False, None
	else:
		token = res.json().get('content', {}).get('token', {}).get('tokenString', '')
		return True, token

def list_data(cookies):
	url = MERCURY_URL
	res = requests.get(url, cookies=cookies)
	if not res.ok:
		print 'Request error, maybe a server error, please retry or contact us directly'
		return 0
	data = res.json()
	print "Hello, there are {} files in your DataYes Mercury VM".format(str(len(data)))
	all_data = [i['name'] for i in data]
	for i in all_data:
		print u'Name: {}'.format(i)

	return all_data

def list_notebook(cookies):
	url = NOTEBOOK_URL
	res = requests.get(url, cookies=cookies)
	if not res.ok:
		print 'Request error, maybe a server error, please retry or contact us directly'
		return 0
	data = res.json()
	print "Hello, there are {} notebooks in your DataYes Mercury VM".format(str(len(data)))
	all_notebook = [i['name'] for i in data]
	for i in all_notebook:
		print u'Name: {}'.format(i)

	return all_notebook
	
def download_notebook(cookies, filename):
	url = DOWNLOAD_NOTEBOOK_URL
	notebook_url = url + '/' + filename
	print u'\nStart download {}'.format(filename),

	with open(filename, 'wb') as f:
	    response = requests.get(notebook_url, cookies=cookies, stream=True)

	    if not response.ok:
	        print u'Something is wrong when download file {} '.format(filename)
	        return 0
	    
            for chunk in response.iter_content(1024 * 100):
		print '...',
	    	f.write(chunk)

def download_file(cookies, filename):
	url = DOWNLOAD_URL
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

def delete_file(cookies, filename):
	url = MERCURY_URL
	deleteurl = url + '/' + filename	
	res = requests.delete(deleteurl, cookies=cookies)

	return res.ok
	