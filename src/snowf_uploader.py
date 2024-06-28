import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import os
import logging
import pandas as pd

ROLE = 'ACCOUNTADMIN'
'TODO: create a staging area'
DATABASE = 'PERSONAL'
SCHEMA = 'PUBLIC'

class SnowfUtility():

    def __init__(self) -> None:
        
        try:
            self.connection = snowflake.connector.connect(
                user        =os.getenv('SNOWF_USER'),
                password    =os.getenv('SNOWF_PW'),
                account     =os.getenv('SNOWF_ACCOUNT'),
                role        = ROLE,
                database    = DATABASE,
                schema      = SCHEMA,
                session_parameters={
                    'QUERY_TAG': 'Load games data'
                }
            )
            
            self.cursor = self.connection.cursor()
        except Exception as error:
            logging.error(f'Snowflake connection error: {error}')

    def _create_table(self, df:pd.DataFrame):

        query   = f'create or replace transient table {DATABASE}.{SCHEMA}.GAMES ( \n' 
        n_cols  = len(df.columns)
        for i, col in enumerate(df.columns):
            query += col + ' VARCHAR'

            if i < n_cols-1:
                query += ', \n'
            else:
                query += '\n)'

        self.cursor.execute(query)

        
    def load_data_to_snowf(self, dframe:pd.DataFrame):
        df         = dframe
        df.columns = [col.upper() for col in df.columns]
        df.fillna('', inplace=True)

        self._create_table(df)

                # 'TODO: refactor'
        results = write_pandas(
            conn = self.connection
            , df = df
            , table_name='GAMES'
            , database=DATABASE
            , schema=SCHEMA
        )
