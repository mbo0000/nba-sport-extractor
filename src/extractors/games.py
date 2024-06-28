from .extractor import Extractor
import json
from datetime import datetime

class GamesExtractor(Extractor):
    def __init__(self, endpoint, param) -> None:
        super().__init__(endpoint, param)
        self.set_url()
        self.set_param()

    def _get_latest_season(self):
        seasons = self.make_request(self.base_url + 'seasons')['response']
        return seasons[-1]

    def set_url(self):
        self.url = self.base_url + self.endpoint
        return self.url

    def set_param(self):
        self.param['season'] = self._get_latest_season()
        return self.param

    def process_data(self, data):

        flatten_data = []
        for game in data['response']:
            flatten = self._flatten(game)
            flatten['_TIME_SYNC'] = datetime.now()
            flatten_data.append(flatten)  

        flatten_data = [game for game in flatten_data if game['status_long'] == 'Finished']

        # converting all val for each key as str for later load into snowflake
        games = []
        for game in flatten_data:
            games.append({k:str(game[k]) for k in game})

        with open('/shared/games.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(games, indent=4))
