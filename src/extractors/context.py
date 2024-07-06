from .extractor import Extractor

class Context():

    def __init__(self, extractor: Extractor):
        self._extractor = extractor

    # getter
    @property
    def extractor(self):
        return self._extractor

    #setter
    @extractor.setter
    def extractor(self, extractor : Extractor):
        self._extractor = extractor

    def extract(self):
        self._extractor.execute()