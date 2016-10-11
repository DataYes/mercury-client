# -*- coding: utf-8 -*-

"""
    uqer.py
    ~~~~~~~~~~~~


    :copyright: (c) 2016 by DataYes Fixed Income Team.
    :Author: taotao.li
"""

import sys
import os
import ConfigParser
import requests


import utils


class Client(object):
    """优矿
    """
    def __init__(self, username='', password='', token=''):
        if not token:
            print 'Welcome, {} ... '.format(username)
            self.isvalid, self.token = utils.authorize_user(username, password)
            self.__cookies = {'cloud-sso-token': self.token}
            if not self.isvalid:
                print 'Sorry, {}, your username or password are not match, authorization failed ...'.format(username)
        else:
            self.isvalid = True
            self.__cookies = {'cloud-sso-token': token}

    def list_data(self):
        if not self.isvalid:
            print 'Sorry, {}, your username or password are not match, authorization failed ...'
            return  

        self.__all_data = utils.list_data(self.__cookies)

    def list_notebook(self):
        if not self.isvalid:
            print 'Sorry, {}, your username or password are not match, authorization failed ...'
            return  

        self.__all_notebook = utils.list_notebook(self.__cookies)
        
    def download_data(self, filename='', download_all=False):
        if not self.isvalid:
            print 'Sorry, {}, your username or password are not match, authorization failed ...'
            return 

        if download_all:
            self.list_data()
            for i in self.__all_data:
                utils.download_file(self.__cookies, i)

        elif type(filename) == list:
            for i in filename:
                utils.download_file(self.__cookies, i)

        elif type(filename) == str:
            utils.download_file(self.__cookies, filename)

        else:
            pass

    def download_notebook(self, filename='', download_all=False):
        if not self.isvalid:
            print 'Sorry, {}, your username or password are not match, authorization failed ...'
            return 

        if download_all:
            self.list_notebook()
            for i in self.__all_notebook:
                utils.download_notebook(self.__cookies, i)

        elif type(filename) == list:
            for i in filename:
                utils.download_notebook(self.__cookies, i)
        
        elif type(filename) in (str, unicode):
            utils.download_notebook(self.__cookies, filename)
        
        else:
            pass

    def backup_data(self):
        self.download_data(download_all=True)

    def backup_notebook(self):
        self.download_notebook(download_all=True)

    def upload_data(self, filepath):
        try:
            f = open(filepath, 'rb')
            files = {'datafile': f}
        except:
            print u"Can not open file at: ".format(filepath)
            return False

        utils.upload_data(files, self.__cookies)
