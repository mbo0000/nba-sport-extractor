from .extractor import Extractor

class GamesExtractor(Extractor):
    def __init__(self, endpoint, param) -> None:
        super().__init__(endpoint, param)
        self.set_url()
        self.set_param()
    
    def _get_latest_season(self):
        '''
        dependency for games endpoint
        '''
        seasons = self.make_request(self.base_url + 'seasons')['response']
        return seasons[-1]

    def set_url(self):
        self.url = self.base_url + self.endpoint
        return self.url

    def set_param(self):
        self.param['season'] = self._get_latest_season()
        return self.param