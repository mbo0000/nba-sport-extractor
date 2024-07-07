import sys
from src.extractors import (
    Context, GamesExtractor, GamesStatsExtractor
)
import logging


entities_map = {
    'games'             : GamesExtractor
    ,'games_statistics' : GamesStatsExtractor
}


def get_args():
    '''
    extract and create arguments dict from cmd
    '''
    if len(sys.argv[1:]) <= 1:
        logging.error("ERROR: No argument was passed in cmd.")
        return None

    it = iter(sys.argv[1:])
    args = dict(zip(it, it))
    return args

def main():
    args = get_args()

    if not args: 
        return
    
    ent         = entities_map[args['--entity']]
    endpoint    = args['--entity']
    database    = args['--database']
    schema      = args['--schema']
    
    context     = Context(ent(
                                endpoint    = endpoint
                                , param     = {}
                                , database  = database
                                , schema    = schema
                ))
    context.extract()

if __name__ == '__main__':
    main()