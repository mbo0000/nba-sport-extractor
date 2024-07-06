from .extractor import Extractor
from src.snowf_util import SnowfUtility 
import time

class GamesStatsExtractor(Extractor):

    def __init__(self, endpoint, param = {}):

        super().__init__(endpoint=endpoint, param=param)
        
        self.endpoint   = endpoint
        self.param      = param
        self.set_url()

    def set_url(self):
        self.url        = self.base_url + self.endpoint.replace('_','/')
        return self.url

    def set_param(self, id):
        self.param['id'] = id 
        return self.param

    def _get_games(self):
        snowf_con = SnowfUtility()
        query = '''
            select 
                id
            from clean.nba.games 
            where true
                and id not in (
                    select id from clean.nba.games_statistics
                )
                and status_long = 'Finished'
        '''

        return snowf_con.query_from_table(query)
        
    def make_request(self, url, params={}):
        
        '''
        check if table exist, if so pull current games ingested
        filter for games not ingested from response data
        make api requests for games not ingested
        write to file 
        '''

        existing_games = [game[0] for game in self._get_games()]
        if not existing_games or len(existing_games) == 0:
            return None

        result = []
        for game in existing_games:

            if not self.is_under_quota_limit():
                raise Exception('Error exceeded daily quota limit')
                
            self.param  = self.set_param(game)
            response    = self._api_call(self.url, self.param)
            response['response'][0]['game_id']  = game
            response['response'][-1]['game_id'] = game
            result.extend(response['response'])
            
            # usage rate 10 requests per minute
            time.sleep(6)

        return result
