from .extractor import Extractor
from src.snowf_util import SnowfUtility 
import time
import logging

class GamesStatsExtractor(Extractor):

    def __init__(self, endpoint, param = {}, database = '', schema = ''):

        super().__init__(endpoint=endpoint, param=param, database=database, schema=schema)
        
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
        '''
        check if table exist, if so pull current games ingested
        filter for games not ingested from response data
        '''

        snowf_con = SnowfUtility()
        query = '''
            select 
                distinct id
            from clean.nba.games 
            where true
                and id not in (
                    select distinct game_id from clean.nba.games_statistics
                )
                and status_long = 'Finished'
        '''
        logging.info("retrieving existing games IDs from games table")
        return snowf_con.query_from_table(query)
        
    def make_request(self):
        
        '''
        make api requests for game stats not yet ingested
        '''

        existing_games = [game[0] for game in self._get_games()]
        if not existing_games or len(existing_games) == 0:
            logging.info('No new game statistics to extract or update.')
            return None

        result  = []
        idx     = 0
        mlen    = len(existing_games)

        while idx < mlen:
            logging.info(f"numbers of games stats to be extract: {idx}/{mlen}")
            
            if not self.is_under_quota_limit():
                logging.error('exceeded daily quota limit')
                break
                
            game       = existing_games[idx]
            self.param = self.set_param(game)
            response   = self._api_call(self.url, self.param)
            games_res  = response['response']

            # skip current game stats if response does not have any result
            if not games_res or response['results'] < 1:
                logging.error(f'Empty result from games_statistics with game ID of {game}')
                logging.error(response['errors'])
                continue

            games_res[0]['game_id']  = game
            games_res[-1]['game_id'] = game
            result.extend(games_res)

            # usage rate buffer
            time.sleep(10)
            idx += 1

        return result
