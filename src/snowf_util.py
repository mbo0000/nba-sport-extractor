import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import os
import logging
import pandas as pd

ROLE = 'ACCOUNTADMIN'

class SnowfUtility():

    def __init__(self, endpoint = '', database= '', schema='') -> None:

        self.database   = database.strip().upper()
        self.schema     = schema.strip().upper()
        self.table      = endpoint.strip().upper()

        try:
            self.connection = snowflake.connector.connect(
                user        = os.getenv('SNOWF_USER'),
                password    = os.getenv('SNOWF_PW'),
                account     = os.getenv('SNOWF_ACCOUNT'),
                role        = ROLE,
                database    = self.database,
                schema      = self.schema,
                session_parameters={
                    'QUERY_TAG': f'Load {self.table} data'
                }
            )
            
            self.cursor = self.connection.cursor()
        except Exception as error:
            logging.error(f'Snowflake connection error: {error}')

    def _create_table(self, df:pd.DataFrame):

        query   = f'create or replace transient table {self.database}.{self.schema}.{self.table} ( \n' 
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
            conn            = self.connection
            , df            = df
            , table_name    = self.table
            , database      = self.database
            , schema        = self.schema
        )

    def query_from_table(self, query):
        data = self.cursor.execute(query)
        return data.fetchall()
