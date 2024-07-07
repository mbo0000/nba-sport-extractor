from abc import abstractmethod
import requests
from requests import RequestException
import logging
import os
from datetime import datetime
import json
from src.snowf_util import SnowfUtility
import pandas as pd
import time


QUOTA           = 95
QUOTA_ENDPOINT  = 'status'

class Extractor:
    
    def __init__(self, endpoint = '', param = {}, database = '', schema = '') -> None:
        self.host        = os.getenv('HOST')
        self.token       = os.getenv('TOKEN')
        self.base_url    = os.getenv('BASE_URL')
        self.endpoint    = endpoint
        self.param       = param
        self.database    = database
        self.schema      = schema
        self.url         = self.base_url + self.endpoint
        self.daily_quota = QUOTA
        self.headers     = {
                        "X-RapidAPI-Key": self.token,
                        "X-RapidAPI-Host": self.host,
                        "Content-Type": "application/json", 
                        "Accept": "application/json"
                    }

    @abstractmethod 
    def set_url(self):
        pass

    @abstractmethod
    def set_param(self):
        pass

    def _flatten(self, input_dict, separator='_', prefix='', skip=[]):

        """
        Recursively flattens a nested dictionary or dictionaries within lists, concatenating keys to 
        reflect the structure of the original nested dictionary.
        """

        if not isinstance(input_dict, dict) and not isinstance(input_dict, list):
            return input_dict

        output_dict = {}
        for key, value in input_dict.items():
            if isinstance(value, dict) and value:
                deeper = self._flatten(value, separator, prefix + key + separator)
                output_dict.update({key2: val2 for key2, val2 in deeper.items()})
            elif isinstance(value, list) and value:
                for _, sublist in enumerate(value, start=1):
                    if key in skip:
                        output_dict[key] = value
                    if isinstance(sublist, dict) and sublist:
                        deeper = self._flatten(sublist, separator, prefix + key + separator)
                        output_dict.update({key2: val2 for key2, val2 in deeper.items()})
                    else:
                        output_dict[prefix + key + separator] = value
            else:
                output_dict[str(prefix) + str(key)] = value
        return {k.removesuffix('_'): v for k, v in output_dict.items()}

    def _api_call(self, url, params = {}):
        '''
        make api request with error handling for rate limit
        '''
        try:
            response = requests.get(url, headers = self.headers, params = params)

            if response.status_code == 429 or response.status_code != 200:
                logging.error(response.json()['errors'])
                while response.status_code == 429:
                    time.sleep(10)
                    response = requests.get(url, headers = self.headers, params = params)

        except RequestException as e:
            logging.error(e)
        
        return response.json()

    def is_under_quota_limit(self):
        '''
        check current quota usage
        '''
        res = self._api_call(self.base_url + QUOTA_ENDPOINT)
        res = res['response']
        print(res)
        if isinstance(res, list) or len(res) == 0 or not res:
            logging.error('Error: reached daily quota')
            return False

        curr_quota = res['requests']['current']

        print(f'current quota: {curr_quota}/{QUOTA}')
        logging.info(f'Current quota is {curr_quota}. Number of limit left: {QUOTA - curr_quota}')
        
        return curr_quota <= self.daily_quota

    def process_data(self, data, file_path):

        if isinstance(data, dict):
            data = data['response']

        flatten_data = []
        for el in data:
            flatten = self._flatten(el)
            flatten['SYNC_TIME'] = datetime.now()
            flatten_data.append(flatten)  

        # converting all val for each key as str for later load into snowflake
        flatten = []
        for el in flatten_data:
            flatten.append({k:str(el[k]) for k in el})

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(flatten, indent=4))

    def make_request(self):
        '''
        send request base on entity, endpoint and params given
        '''
        if not self.token:
            raise Exception('Error missing auth token')

        if not self.is_under_quota_limit():
            return None

        response = self._api_call(self.url, self.param)
        return response

    def execute(self):

        logging.info(f'Making request to: {self.url}')
        data = self.make_request()
        print(f"data size: {len(data)}")
        if not data or len(data) == 0:
            logging.error(f'Empty result from {self.endpoint}')
            return None

        file_path = os.getcwd() + '/out_files/' + self.endpoint +'.json'
        self.process_data(data, file_path)

        # upload to snowflake
        dframe      = pd.read_json(file_path)
        snowf_util  = SnowfUtility(endpoint=self.endpoint, database=self.database, schema=self.schema)
        snowf_util.load_data_to_snowf(dframe)

        os.remove(file_path)