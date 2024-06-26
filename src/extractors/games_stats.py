from .extractor import Extractor

class GamesStatsExtractor(Extractor):
    def __init__(self, entity, param = {}) -> None:

        super().__init__(entity=entity, param=param)
