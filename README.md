# nba-sport-extractor
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.x-green)
![Snowflake](https://img.shields.io/badge/Snowflake-%23f3f1ff)
![Docker](https://img.shields.io/badge/Docker-%2B-blue)

## Introduction

Welcome to the NBA data extraction and load repository. This project is an essential utility that enables seamless NBA games and statistics data extraction via an API and uploads to Snowflake programmatically. This program is designed to be executed locally or by Apache Airflow over a network.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)

## Features

- **Data Extraction**: Efficiently pull data from any API endpoint.
- **Data Upload**: Securely upload data to Snowflake using the Snowflake Python connector.
- **Modular Design**: Easily integrate with Apache Airflow or other orchestration tools.

## Architecture

![Diagram](https://github.com/mbo0000/nba-sport-extractor/blob/main/img/diagram.png)

1. **API Data Extraction**: Retrieves data from specified API endpoints.
2. **Data Transformation**: Prepare the data for insertion into Snowflake (if applicable).
3. **Upload to Snowflake**: dump the transformed data into Snowflake staging area.
4. **Integration with Apache Airflow**: OPTIONAL - The program is executed via Airflow, allowing for scheduling and monitoring.

## Installation

### Prerequisites

- Python 3.9+
- Snowflake Account
- Apache Airflow (2.x recommended)
- Docker
- [API Sport Account](https://api-sports.io)

### Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/mbo0000/nba-sport-extractor.git
    cd nba-sport-extractor
2. Run container and install dependencies:
    ```sh
    docker compose up -d
3. Create Snowflake database and schema
4. Create .env file and provide env credentials for both Snowflake and API Sport. Example: 
    ```
    SNOWF_USER=foo
    SNOWF_PW=foo
    SNOWF_ACCOUNT=foo
    ```
    
## Usage
### Running the script
To run the script manually for [nba games endpoint](https://api-sports.io/documentation/nba/v2#tag/Games):
1. run command
    ```sh
    python main.py --entity games --database your-db-name --schema your-schema-name
2. replace --entity games with --entity games_statistics for [games statistics](https://api-sports.io/documentation/nba/v2#tag/Games/operation/get-games-statistics). 

OPTIONAL: Integrating with Airflow
1.  Define a DAG in Airflow to call this script.
2.  Ensure all network configurations allow Airflow to access the machine where this program runs.
Here is an example Airflow DAG snippet to execute this:

```
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {
    'owner': 'yourname',
    'start_date': datetime(2024, 1, 1),
}

with DAG('data_extraction_dag', default_args=default_args, schedule_interval='@daily') as dag:
    extract_and_upload = BashOperator(
        task_id='extract_and_upload',
        bash_command  = f'docker exec nba-sport-extractor-app-1 python main.py '\
                                f' --entity games'\
                                f' --database your-db-name'\
                                f' --schema your-schema-name'
    )

    extract_and_upload
```

For a detail Airflow DAG using this project, visit [NBA Sport Airflow](https://github.com/mbo0000/nba-sport-airflow) repo.

## Future work & improvements
To expand the project further and create a robust data pipeline:
1. Extract additional entities such as players, players statistics, teams and team statistics. 
2. Capture Slow Changing Dimensions(SCD) through modeling techniques(insert, update, delete) in the source tables.
3. OPTIONAL: Thinking about scaling and scaling strategy. In this project, data is saved to file locally and load into Snowflake. While this works for smaller data set, it will not work for larger data down the road. This may not be applicable for a small scale project such as this.
4. OPTIONAL: Host on a cloud service provider, such as  AWS.
5. Implement CI/CD 


## Contact
For additional information or questions, please contact:
- Email: mbo0000da@gmail.com
- ​[LinkedIn](https://www.linkedin.com/in/minh-b-0bb0628b/)
- [​GitHub](https://github.com/mbo0000)

This project is open source and free for use. Thank you for checking out this project!
