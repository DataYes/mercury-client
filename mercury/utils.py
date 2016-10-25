# -*- coding: utf-8 -*-

"""
    utils.py
    ~~~~~~~~~~~~


    :copyright: (c) 2016 by DataYes Fixed Income Team.
    :Author: taotao.li
"""

import sys
import os
import ConfigParser
import urllib
import requests


AUTHORIZE_URL = "https://gw.wmcloud.com/usermaster/authenticate.json"
MERCURY_URL = 'https://gw.wmcloud.com/mercury/api/databooks'
DOWNLOAD_DATA_URL = 'https://gw.wmcloud.com/mercury/databooks'
NOTEBOOK_URL = 'https://gw.wmcloud.com/mercury/api/notebooks?recursion'
DOWN_NOTEBOOK_URL = 'https://gw.wmcloud.com/mercury/files'
FOLDERS = []
LOCAL_PATH = './'


def authorize_user(user, pwd):
    url = AUTHORIZE_URL

    ### 2 user type
    if '@' in user:
        user_prefix, tenant = user.split("@")
    else:
        user_prefix, tenant = user, ''

    data_type1 = dict(username=user_prefix, password=pwd, tenant=tenant)
    data_type2 = dict(username=user, password=pwd)

    def user_type(data=None):
        res = requests.post(url, data)
        if not res.ok or not res.json().get('content', {}).get('accountId', 0):
            return False, None
        else:
            token = res.json().get('content', {}).get('token', {}).get('tokenString', '')
            return True, token

    valid_1, token_1 = user_type(data_type1)
    valid_2, token_2 = user_type(data_type2)

    if not valid_1 and not valid_2:
        return False, None
    else:
        token = token_1 if token_1 else token_2
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
    global FOLDERS
    url = NOTEBOOK_URL
    res = requests.get(url, cookies=cookies)
    if not res.ok:
        print 'Request error, maybe a server error, please retry or contact us directly'
        return 0
    data = res.json()
    all_notebook = []
    for i in data:
        if i['type'] == 'directory':
            FOLDERS.append(i['name'])
            for j in i['children']:
                all_notebook.append(u'{}/{}'.format(i['name'], j['name']))
        elif i['type'] == 'notebook':
            all_notebook.append(u'{}'.format(i['name']))
        else:
            pass
    print "Hello, there are {} notebooks in your DataYes Mercury VM".format(str(len(all_notebook)))
    for i in all_notebook:
        print u'Name: {}'.format(i)

    return all_notebook
    
def download_notebook(cookies, filename):
    global FOLDERS
    url = DOWN_NOTEBOOK_URL
    folders = set(FOLDERS)
    notebook_url = url + '/' + urllib.quote(filename.encode('utf-8'))
    print u'\nStart download {}'.format(filename),
    print notebook_url

    filename = filename.split('/')[-1]
    with open(LOCAL_PATH + filename, 'wb') as f:
        response = requests.get(notebook_url, cookies=cookies, stream=True)

        if not response.ok:
            print u'Something is wrong when download file {} '.format(filename)
            return 0
        
        for chunk in response.iter_content(1024 * 100):
            print '...',
            f.write(chunk)
    print u'\nDone download {}'.format(filename)


def download_file(cookies, filename):
    url = DOWNLOAD_DATA_URL
    dataurl = url + '/' + filename          
    print '\nStart download {}'.format(filename),

    with open(filename, 'wb') as f:
        response = requests.get(dataurl, cookies=cookies, stream=True)

        if not response.ok:
            print u'Something is wrong when download file {} '.format(filename)
            return 0
        
        for chunk in response.iter_content(1024 * 100):
            print '...',
            f.write(chunk)
    print '\nDone download {}'.format(filename)

def upload_data(files, cookies):
    r = requests.post(MERCURY_URL, files=files, cookies=cookies)
    print r.text
