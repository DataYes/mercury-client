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
    # if '@' in user:
        # user, tenant = user.split("@") 
    # else:
        # return False, None
    # data = dict(username=user, password=pwd, tenant=tenant)
    data = dict(username=user, password=pwd)
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

def order_delay(account_id, date, orders, cookies):
    try:
        sent_dict = {}
        sent_dict["AccountId"] = account_id
        sent_dict["Date"] = date
        sent_dict["Orders"] = orders
        for order in sent_dict["Orders"]:
            if order.has_key('Price'):
                order["Algorithm"] = 'LIMIT'
            else:
                order["Algorithm"] = 'MARKET'
            order["StartTime"] = None
            order["EndTime"] = None
        resp = requests.post("https://gw.wmcloud.com/pms_mom/api2/order/placeDelay", cookies=cookies, json=sent_dict)
        print resp.text
    except Exception, e:
        raise e