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
- [High Level Design](#high-level-design)
- [Code Design Patterns](#code-design-patterns)
- [Installation](#installation)
- [Usage](#usage)
- [Future Works & Improvements](#future-works-&-improvements)
- [Limitation](#limitation)
- [Contact](#contact)

## Features

- **Data Extraction**: Efficiently pull data from any API endpoint.
- **Data Upload**: Securely upload data to Snowflake using the Snowflake Python connector.
- **Modular Design**: Easily integrate with Apache Airflow or other orchestration tools.

## High Level Design

![Diagram](https://github.com/mbo0000/nba-sport-extractor/blob/main/img/diagram.png)

1. **API Data Extraction**: Retrieves data from specified API endpoints.
2. **Data Formatting**: Prepare the data for insertion into Snowflake (if applicable).
3. **Upload to Snowflake**: dump the transformed data into Snowflake staging area.
4. **Integration with Apache Airflow**: OPTIONAL - The program is executed via Airflow, allowing for scheduling and monitoring.

## Code Design Patterns

![Diagram](https://github.com/mbo0000/nba-sport-extractor/blob/main/img/code_pattern.png)

The code base design is subscribed to a hybrid model of Factory and Strategy patterns. All entities in the NBA Sport API follow a consistent pattern for data extraction, formatting, and uploading. Each entity, such as games or game_statistics, implements a standard set of methods and interfaces. When [main.py](https://github.com/mbo0000/nba-sport-extractor/blob/main/main.py) is called externally, such as via Airflow, it determines which extractor subclass to use based on the provided arguments. During runtime, the behavior of each stage is encapsulated within individual subclasses, which are managed by the [Context](https://github.com/mbo0000/nba-sport-extractor/blob/main/src/extractors/context.py) manager. 

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
2. Create source and target databases and schemas in Snowflake:
    - SOURCE: 
        - database: RAW
        - schema: NBA_DUMP
    - TARGET:
        - database: CLEAN
        - schema: NBA
3. Create .env file and provide env credentials for both Snowflake and API Sport. Example: 
    ```
    SNOWF_USER=foo
    SNOWF_PW=foo
    SNOWF_ACCOUNT=foo
    
    HOST=v2.nba.api-sports.io
    TOKEN=foo
    BASE_URL=foo
    ```
4. Create container and install dependencies:
    ```sh
    docker build -t nba-extractor-image .
    docker compose up -d
    
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

For a complete data pipeline using this project, visit [NBA Sport Airflow](https://github.com/mbo0000/nba-sport-airflow) repo.

## Future work & improvements
1. Extract additional entities such as players, players statistics, teams and team statistics. 
2. Capture Slow Changing Dimensions(SCD) through modeling techniques(insert, update, delete) in the source tables.
4. OPTIONAL: Host on a cloud service provider, such as  AWS.
5. Implement CI/CD
6. Refine/expand roburst logs for ease of debugging.  

## Limitation
The NBA Sport account for this project is a free tier account with a daily usage limit of 100 and a maximum of 10 requests per minute. To adhere to these rate limits, some tables may not have the latest data immediately.

## Contact
For additional information or questions, please contact:
- Email: mbo0000da@gmail.com
- ​[LinkedIn](https://www.linkedin.com/in/minh-b-0bb0628b/)
- [​GitHub](https://github.com/mbo0000)

Thank you for checking out this project!
