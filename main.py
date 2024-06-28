import sys
from src.extractors import (
    Context, GamesExtractor, GamesStatsExtractor
)

entities_map = {
    'games': GamesExtractor
}


def get_args():
    if len(sys.argv[1:]) <= 1:
        return None

    it = iter(sys.argv[1:])
    args = dict(zip(it, it))
    return args

def main():
    args = get_args()

    if not args: 
        return
    
    ent = entities_map[args['--entity']]
    endpoint = args['--entity']
    context = Context(ent(endpoint=endpoint, param={}))
    context.extract()

if __name__ == '__main__':
    main()