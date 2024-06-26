import snowflake.connector
import pandas as pd
import os
import logging

ROLE = 'ACCOUNTADMIN'
DATABASE = 'PERSONAL'
SCHEMA = 'PUBLIC'

class SnowfUtility():

    def __init__(self) -> None:
        
        try:
            self.connection = snowflake.connector.connect(
                user=os.getenv('SNOWF_USER'),
                password=os.getenv('SNOWF_PW'),
                account=os.getenv('SNOWF_ACCOUNT'),
                role = ROLE,
                database = DATABASE,
                schema = SCHEMA,
                session_parameters={
                    'QUERY_TAG': 'TestConnection'
                }
            )
            
            self.cursor = self.connection.cursor()
        except Exception as error:
            logging.error(f'Snowflake connection error: {error}')

    def _execute_query(self, query):
        pass
