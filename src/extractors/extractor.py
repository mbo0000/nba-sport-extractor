import requests
from requests import RequestException
import json
import logging
import os

BASE_URL        = 'https://v2.nba.api-sports.io/'
QUOTA           = 95
QUOTA_ENDPOINT  = 'status'

class Extractor:
    
    def __init__(self, entity, param = {}) -> None:
        self.host        = os.getenv('HOST')
        self.token       = os.getenv('TOKEN')
        self.entity      = entity
        self.param       = param
        self.base_url    = BASE_URL
        self.url         = BASE_URL + entity
        self.daily_quota = QUOTA
        self.headers     = {
                        "X-RapidAPI-Key": self.token,
                        "X-RapidAPI-Host": self.host,
                        "Content-Type": "application/json", 
                        "Accept": "application/json"
                    }

    def _flatten(self, input_dict, separator='_', prefix='', skip=[]):

        """
        Recursively flattens a nested dictionary or dictionaries within lists, concatenating keys to 
        reflect the structure of the original nested dictionary.

        Parameters:
            input_dict (dict): The dictionary to flatten.
            separator (str, optional): The string used to separate key components in the flattened keys.
                                    Defaults to '_'.
            prefix (str, optional): A prefix used for keys; useful in recursive calls to maintain the
                                    current path of nested keys. Defaults to an empty string.
            skip (list, optional): A list of keys to skip the flattening process for lists contained 
                                under these keys. Defaults to an empty list.
            
        Returns:
            dict: A new dictionary with flattened keys

        Examples:
            # Flattening a dictionary with nested dictionaries and lists
            sample_input = {
                'a': {
                    'b': {
                        'c': 1,
                        'd': 2
                    }
                },
                'e': [3, {'f': 4}]
            }
            print(_flatten(sample_input))
            # Output: {
                'a_b_c': 1,
                'a_b_d': 2,
                'e': [3, {'f': 4}]
            }
            # Note: List under 'e' is not fully flattened because it contains both simple value
        """

        if not isinstance(input_dict, dict) or not isinstance(input_dict, list):
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

        try:
            response = requests.get(url, headers = self.headers, params = params)
            if response.json()['errors']:
                logging.error(response.json()['errors'])
            return response.json()
        except RequestException as e:
            logging.error(e)
        
        return None

    def _get_current_quota(self):
        '''
        check current quota usage
        '''
        res         = self._api_call(self.base_url + QUOTA_ENDPOINT)
        curr_quota  = res['response']['requests']['current']
        logging.info(f'Current quota is {curr_quota}. Number of limit left: {QUOTA - curr_quota}')
        return curr_quota
        

    def make_request(self, url, params = {}):
        '''
        send request base on entity, endpoint and params given
        '''
        if not self.token:
            raise Exception('Error missing auth token')

        curr_quota = self._get_current_quota()
        if curr_quota >= self.daily_quota:
            logging.error(f'Error current quota: {curr_quota}/{self.daily_quota}')
            raise Exception('Error exceeded daily quota limit')

        response = self._api_call(url, params)
        return response

    def execute(self):
        logging.info(f'Making request to: {self.url}')
        data = self.make_request(self.url, self.param)
        if not isinstance(data['response'], list):
            logging.info(f'Empty result from {self.entity}')
            return data['response']

        flatten_data = []
        for entity in data['response']:
            flatten_data.append(self._flatten(entity))

        'TODO: handle output'
        print(flatten_data)