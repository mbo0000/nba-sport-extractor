import sys
from src.extractors import (
    Context, GamesExtractor, GamesStatsExtractor
)
from src.snowf_uploader import SnowfUtility
import os
import pandas as pd

entities_map = {
    'games': GamesExtractor
    ,'games_stats':GamesStatsExtractor
}


def get_args():
    '''
    extract and create arguments dict from cmd
    '''
    if len(sys.argv[1:]) <= 1:
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
    
    context     = Context(ent(endpoint=endpoint, param={}))
    context.extract()

    file_path   = '/shared/'+ endpoint +'.json'
    dframe      = pd.read_json(file_path)

    snowf_util  = SnowfUtility(endpoint=endpoint, database=database, schema=schema)
    snowf_util.load_data_to_snowf(dframe)

    os.remove(file_path)

if __name__ == '__main__':
    main()