import requests
import json
import time
import threading
import logging
import urllib3
import os
import binascii

urllib3.disable_warnings()
logging.basicConfig(level=logging.INFO)


class pyPLCn(object):

    def __init__(self):
        self._run_flag = False
        self.s = requests.Session()
        self._poll_time = 500
        self._ip = ''
        self._session_id = ''
        self.vars_group = ''
        self.vars = []
        self._worker_thread = threading.Thread(target=self._task)
        self.vars = ''
        self.read_vars = []
        self._status_code = 0
        self._clientState = ''
        self._auth_code = ''
        self._access_token = ''
        self._login = ''
        self._password = ''
        self._write = bool(False)
        self._set_var = []
        self._set_var_value = ''
        self._connected = False

    def __del__(self):
        self._run_flag = False

    def close(self):
        """Close connection
        :rtype: None
        """
        self._run_flag = False
        self.s.close()

    def _get_session_id(self, ip=''):
        try:
            response = self.s.post('https://{}:443/_pxc_api/v1.2/sessions/'.format(ip), data='stationID=99', verify=False)
            if int(response.status_code) == 201:
                self._session_id = json.loads(response.text)['sessionID']
                logging.info('Session ID = {}'.format(self._session_id))
                self._connected = True
            else:
                logging.error('Error get session ID! {}'.format(dict(response.text))['error']['details'][0]['reason'])
                self._connected = False
        except Exception as e:
            self._connected = False
            print(e)

    def _get_vars_group(self, ip=''):
        try:
            temp_json = json.loads('{"sessionID": "", "pathPrefix": "Arp.Plc.Eclr/", "paths": []}')
            temp_json['sessionID'] = self._session_id
            temp_json['paths'] = self.vars
            request = str(temp_json).replace("""'""", '''"''')
            headers = {'Authorization': 'Bearer {}'.format(self._access_token)}
            response = self.s.post('https://{}:443/_pxc_api/v1.2/groups/'.format(ip), headers=headers,
                                   data=request, verify=False)
            if int(response.status_code) == 201:
                self.vars_group = json.loads(response.text)['id']
                logging.info('Vars group = {}'.format(self.vars_group))
                self._connected = True
            else:
                logging.error('Error set vars! >>{}<<'.format(json.loads(response.text)
                                                              ['error']['details'][0]['reason']))
                self._connected = False
        except Exception as e:
            self._connected = False
            print(e)

    def _get_clientState(self):
        self._clientState = str(hex(int(binascii.b2a_hex(os.urandom(8)), 16)))[2::]
        logging.info('Client State = {}'.format(self._clientState))

    def _get_clientCode(self):
        try:
            temp_json = json.loads('{"response_type":"code","state":"","scope":"variables"}')
            temp_json['state'] = self._clientState
            request = str(temp_json).replace("""'""", '''"''')
            response = self.s.post('https://{}:443/_pxc_api/v1.2/auth/auth-token'.format(self._ip), data=request, verify=False)
            if int(response.status_code) == 200:
                self._auth_code = json.loads(response.text)['code']
                logging.info('Auth code = {}'.format(self._auth_code))
                self._connected = True
            else:
                logging.error('Error get auth code! {}'.format(json.loads(response.text)
                                                              ['error']['details'][0]['reason']))
                self._connected = False
        except Exception as e:
            self._connected = False
            print(e)

    def _authorization(self, login='', password=''):
        try:
            temp_json = json.loads('{"code":"","grant_type":"authorization_code","username":"","password":"","state":""}')
            temp_json['code'] = self._auth_code
            temp_json['username'] = login
            temp_json['password'] = password
            temp_json['state'] = self._clientState
            request = str(temp_json).replace("""'""", '''"''')
            response = self.s.post('https://{}:443/_pxc_api/v1.2/auth/access-token'.format(self._ip), data=request,
                                   verify=False)
            if int(response.status_code) == 200:
                self._access_token = json.loads(response.text)['access_token']
                logging.info('Access token = {}'.format(self._access_token))
                self._connected = True
            else:
                logging.error('Error get access token! {}'.format(json.loads(response.text)
                                                              ['error']['details'][0]['reason']))
                self._connected = False
        except Exception as e:
            self._connected = False
            print(e)

    def set_var_names(self, vars=[]):
        """Setting variables to work with them
        :param vars: list of variable names in format - "['LevelMinimum', 'LevelMaximum', 'Robot.Test_Var']".
        :rtype: None
        """
        self.vars = vars

    def connect(self, ip='127.0.0.1', login='', password='', poll_time=100):
        """Connect to PLC. If you not use authentication leave login and password field blank
        :param ip: IP address of PLC.
        :param login: username with "EHmiViewer", "EHmiChanger" rights.
        :param password: password from account.
        :param poll_time: time of update variables.
        :rtype: None
        """

        self._ip = ip
        self._poll_time = poll_time
        self._get_session_id(ip=self._ip)
        if not login == '' and not password == '':
            self._login = login
            self._password = password
            self._get_clientState()
            self._get_clientCode()
            self._authorization(login=self._login, password=self._password)
        self._get_vars_group(ip=self._ip)
        if not self._run_flag:
            self._run_flag = True
            self._worker_thread.setDaemon(True)
            self._worker_thread.start()

    def is_connected(self):
        """Check connection status.
        :rtype: bool
        """
        return self._connected

    def _task(self):
        while self._run_flag:
            try:
                headers = {'Authorization': 'Bearer {}'.format(self._access_token)}
                response = self.s.get('https://{0}:443/_pxc_api/v1.2/groups/{1}/?sessionID={2}&'.format(self._ip,
                                                                                                        self.vars_group,
                                                                                                        self._session_id),
                                      verify=False, headers=headers)
                self._status_code = int(response.status_code)
                if self._status_code == 200:
                    self.read_vars = json.loads(response.text)['variables']
                    self._connected = True
                else:
                    self._connected = False
            except Exception as e:
                self._connected = False
                self.s.close()
                logging.error('Connection error! {}'.format(e))
            finally:
                if not self._connected and self._run_flag:
                    for var in self.read_vars:
                        var['value'] = None
                    logging.error('Connection error, trying to reconnect in 5 seconds!')
                    time.sleep(5)
                    self.connect(self._ip, self._login, self._password, self._poll_time)
                time.sleep(float(self._poll_time / 1000))

    def get_var(self, var_name=''):
        """Get one variable from PLC by name.

        :param var_name: Name of variable HMI tag declarated in PLC.
        :rtype: str or None
        """
        if self._status_code == 200:
            for var in self.read_vars:
                if var_name == var['path']:
                    break
            return var['value']
        else:
            pass

    def set_var(self, var_name='', value=''):
        """Set one variable in PLC by name.

        :param var_name: Name of variable HMI tag declarated in PLC.
        :param value: Value in string format like "True" "10" etc.
        :rtype: None
        """
        if self._connected:
            temp_json = json.loads('{"sessionID": "", "pathPrefix": "Arp.Plc.Eclr/", "variables":""}')
            temp_json['sessionID'] = self._session_id
            temp_json['variables'] = [{"path": str(var_name), "value": str(value).lower(),
                                       "valueType": "Constant"}]
            request = str(temp_json).replace("""'""", '''"''')
            headers = {'Authorization': 'Bearer {}'.format(self._access_token)}
            response = self.s.put('https://{}:443/_pxc_api/v1.2/variables/'.format(self._ip), data=request,
                                  verify=False, headers=headers)
            self._status_code = int(response.status_code)
            if self._status_code == 200:
                self._connected = True
            else:
                self._connected = False
        else:
            pass