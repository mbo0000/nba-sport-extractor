from .extractor import Extractor

class GamesStatsExtractor(Extractor):
    def __init__(self, endpoint, param = {}) -> None:

        super().__init__(endpoint=endpoint, param=param)
        
        self.endpoint = endpoint
        self.param = param