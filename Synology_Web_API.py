import os
import logging
import getpass

import requests
from requests.compat import urljoin

logging.basicConfig(level=logging.INFO)

class SynologyDiskStation(object):
    def __init__(self, ip='', port=None, secure=False,
        name=''):

        self.ip = ip if ip else '192.168.1.100'
        self.skip_verify = False
        if self.ip.startswith('192.168'):
            self.skip_verify = True
        self.port = port if port else 5000
        self.name = name if name else 'DiskStation'
        self.sid=''

        self.base_url = '{h}://{ip}:{port}/webapi/'.format(
            h='https' if secure else 'http',
            ip=ip, port=port)
        self.auth_url = urljoin(self.base_url, 'auth.cgi')
        self.auth_params = {
            'api': 'SYNO.API.Auth',
            'version': '7',
            'method': 'login',
            'account': '',
            'passwd': '',
            'session': self.name,
            'format': 'sid'
            }
        self.api_base_url = urljoin(self.base_url, self.name+'/')
        
    def login(self, ac='admin', pw=''):
        print(f'Account: {ac}')
        pw = getpass.getpass() if not pw else pw
        self.auth_params['account'] = ac
        self.auth_params['passwd'] = pw
        if self.skip_verify:
            r_json = requests.get(
                self.auth_url,
                params=self.auth_params,
                verify=False).json()
        else:
            r_json = requests.get(
                self.auth_url,
                params=self.auth_params,
                ).json()
        if r_json['success']:
            self.sid = r_json['data']['sid']
            logging.info('Login {ss} Success.'.format(ss=self.name))
            logging.debug('Session {ss} ID: {sid}'.format(
                ss=self.name, sid=self.sid))
        else:
            logging.info('Login {ss} Fault.'.format(ss=self.name))
            logging.debug('Session {ss} ID: {sid}'.format(
                ss=self.name, sid=self.sid))


class SynologyDownloadStation(SynologyDiskStation):
    def __init__(self, ip='192.168.1.100', port=5000, secure=False,
        name='DownloadStation'):
        super(SynologyDownloadStation, self).__init__(ip, port, secure, name)

        self.base_download_folder = 'home'

    def uploadTorrent(self, torrent_uri, destination=''):
        # bt 目的地 path 處理
        destination =\
            self.base_download_folder if not destination else destination
        if destination.startswith('/'):
            destination = destination.lstrip('/')

        self.task_url = urljoin(self.api_base_url, 'task.cgi')
        self.task_params = {
            'api': 'SYNO.{n}.{m}'.format(n=self.name, m='Task'),
            'version': '1',
            'method': 'create',
            'uri': torrent_uri,
            'destination': destination,
            '_sid': self.sid
            }
        r_json = requests.get(
            self.task_url, params=self.task_params).json()
        logging.info('Update Success?: {b}'.format(b=r_json['success']))


class SynologyFileStation(SynologyDiskStation):
    def __init__(self, ip='192.168.1.100', port=5000, secure=False,
        name='FileStation'):
        super(SynologyFileStation, self).__init__(ip, port, secure, name)

    def createFolder(self, destination):
        p, n = os.path.split(destination)

        self.entry_url = urljoin(self.base_url, 'entry.cgi')
        self.entry_params = {
            'api': 'SYNO.{n}.{m}'.format(n=self.name, m='CreateFolder'),
            'version': '2',
            'method': 'create',
            'folder_path': [p],
            'name': [n],
            '_sid': self.sid
            }
        r_json = requests.get(
            self.entry_url, params=self.entry_params).json()
        logging.info('Create Folder Success?: {b}'.format(b=r_json['success']))
