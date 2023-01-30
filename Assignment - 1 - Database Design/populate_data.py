import os
import kaggle
import pandas as pd
from getpass import getpass
from mysql.connector import connect, Error

import queries
from utils import execute_and_commit, random_email_gen, insert_data, styled_print, fetch_data


# Static Variables
DATASET_PATH = "./data/"
DATASET_ID = "ahmedshahriarsakib/uber-eats-usa-restaurants-menus"

# # Download data from kaggle
styled_print(text=f"Downloading {DATASET_ID}", header=True)

# kaggle.api.authenticate()
# kaggle.api.dataset_download_files(DATASET_ID,
#                                   path=DATASET_PATH, unzip=True)

# Extract and Clean Reastaurant Data
styled_print(
    text=f"Extracting and Cleaning Data for Restaurants Table", header=True)
reastaurant_data = {}
reastaurants_df = pd.read_csv(os.path.join(DATASET_PATH, "restaurants.csv"))
reastaurant_data["Email"] = [random_email_gen(
    7) for i in range(reastaurants_df.shape[0])]
for key, value in queries.reastaurant_table_mapping.items():
    reastaurant_data[key] = reastaurants_df[value]
reastaurant_data = pd.DataFrame.from_dict(reastaurant_data)
print(reastaurant_data.info())

# Extract Menu Item Data
styled_print(
    text=f"Extracting and Cleaning Data for MenuItems Table", header=True)
menu_item_data = {}
menu_item_df = pd.read_csv(os.path.join(DATASET_PATH, "restaurant-menus.csv"))
menu_item_data["ItemID"] = [i+1 for i in range(menu_item_df.shape[0])]
for key, value in queries.menu_items_table_mapping.items():
    menu_item_data[key] = menu_item_df[value]
menu_item_data = pd.DataFrame.from_dict(menu_item_data)
print(menu_item_data.info())


# Connect to Database
styled_print(
    text=f"Connecting to Database", header=True)
try:
    connection = connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database="ubereats"
    )
    cursor = connection.cursor()
except Error as e:
    print(e)


# Create Tables
execute_and_commit(
    queries.create_customer_table_query, connection, cursor)
execute_and_commit(queries.create_reastaurant_table_query, connection, cursor)
execute_and_commit(queries.create_menu_items_table_query, connection, cursor)
execute_and_commit(queries.create_drivers_table_query, connection, cursor)
execute_and_commit(queries.create_orders_table_query, connection, cursor)
execute_and_commit(queries.create_deliveries_table_query, connection, cursor)

# Populate the Restaurants Table
insert_data(
    data_dict=reastaurant_data, table="Restaurants",
    cursor=cursor, connection=connection)

# Populate the MenuItems Table
insert_data(
    data_dict=menu_item_data, table="MenuItems",
    cursor=cursor, connection=connection
)


# Query Table
all_restaurants = fetch_data(
    query="SELECT * FROM `Restaurants`",
    cursor=cursor
)
all_menu_items = fetch_data(
    query="SELECT * FROM `MenuItems`",
    cursor=cursor
)

for i in all_restaurants:
    print(i)
