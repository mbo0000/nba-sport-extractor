from .extractor import Extractor

class GamesExtractor(Extractor):
    def __init__(self, entity, param = {}) -> None:

        super().__init__(entity=entity, param=param)
