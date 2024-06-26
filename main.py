
from src.extractors import (
    Context, GamesExtractor, GamesStatsExtractor
)

# entities_map = {
#     'games': GamesExtractor
# }

context = Context(GamesExtractor('seasons'))
context.extract()