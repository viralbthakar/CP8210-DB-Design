# Relational Database Creation for Uber Eats

## Installation
- Create Conda Environment
```
conda create -n ubereats-db python=3.8.8
```
- Activate Environment
```
source activate ubereats-db
```
- Install Packages
```
pip install -r requirements.txt
```

## Connecting to Kaggle API
- Install kaggle package.
    ```
        pip install kaggle
    ```
- Generate api token and set it up.
    - To use the Kaggle API, sign up for a Kaggle account at https://www.kaggle.com.
    - Then go to the `Account` tab of your user profile and select `Create API Token`.
        - This will trigger the download of `kaggle.json`, a file containing your API credentials.
    - Execute following commands to move file 
    ```
        mkdir - p ~/.kaggle
        mvl kaggle.json ~/.kaggle/
        ls ~/.kaggle
        chmod 600 ~/.kaggle/kaggle.json
    ```

## Create Database
```
CREATE DATABASE IF NOT EXISTS ubereats;
```

## Create Tables and Populate Data
There are two options to create table.
1. Using Python Script (Recommended)
    - Execute `python populate_data.py`
2. Using SQL Script
    - Execute commands from `uber_eats_db_creation.sql`

## Run Test Queries
To execute all the test queries mentioned in our report execute
```
python test_queries.py
```
