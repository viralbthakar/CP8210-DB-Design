import os
import kaggle
import pandas as pd
from getpass import getpass
from mysql.connector import connect, Error

import queries
from utils import execute_and_commit, random_email_gen, insert_data, styled_print, fetch_data, create_customers, create_orders, create_deliveries


# Static Variables
DATASET_PATH = "./data/"
DATASET_ID = "ahmedshahriarsakib/uber-eats-usa-restaurants-menus"
NUM_CUSTMERS = 10000
NUM_DRIVERS = 1000
NUM_ORDERS = 10000
NUM_DELIVERY = 10000


# Download data from kaggle
styled_print(text=f"Downloading {DATASET_ID}", header=True)
kaggle.api.authenticate()
kaggle.api.dataset_download_files(DATASET_ID,
                                  path=DATASET_PATH, unzip=True)


# Create Random Customers to Populate Customers Table
styled_print(text=f"Creating {NUM_CUSTMERS} Customer Profiles", header=True)
customer_data = create_customers(NUM_CUSTMERS)
print(customer_data.info())

# Create Random Customers to Populate Customers Table
styled_print(text=f"Creating {NUM_CUSTMERS} Driver Profiles", header=True)
driver_data = create_customers(NUM_DRIVERS, driver=True)
print(driver_data.info())

# Extract and Clean Reastaurant Data to Populate Restaurants Table
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


# Extract Menu Item Data to Populate MenuItems Table
styled_print(
    text=f"Extracting and Cleaning Data for MenuItems Table", header=True)
menu_item_data = {}
menu_item_df = pd.read_csv(os.path.join(DATASET_PATH, "restaurant-menus.csv"))
menu_item_data["ItemID"] = [i+1 for i in range(menu_item_df.shape[0])]
for key, value in queries.menu_items_table_mapping.items():
    menu_item_data[key] = menu_item_df[value]
menu_item_data = pd.DataFrame.from_dict(menu_item_data)
print(menu_item_data.info())


# Randomly sample 100000 elements from your dataframe
styled_print(
    text=f"Sampling 100000 elements for MenuItems Table", header=True)
menu_item_data = menu_item_data.sample(n=100000)
print(menu_item_data.info())

# Create Random Orders to Populate Orders Table
styled_print(text=f"Creating {NUM_ORDERS} Orders", header=True)
order_data = create_orders(
    num_orders=NUM_ORDERS,
    cust_ids=list(customer_data["CustomerID"]),
    rest_ids=list(reastaurant_data["RestaurantID"]),
    item_ids=list(menu_item_data["ItemID"]))
print(order_data.info())

# Create Random Deliveries to Populate Deliveries Table
styled_print(text=f"Creating {NUM_DELIVERY} Deliveries", header=True)
delivery_data = create_deliveries(
    num_deliveries=NUM_DELIVERY,
    order_ids=list(order_data["OrderID"]),
    driver_ids=list(driver_data["DriverID"]))
print(delivery_data.info())

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


# Populate the Customers Table
insert_data(
    data_dict=customer_data, table="Customers",
    cursor=cursor, connection=connection)


# Populate the Driver Table
insert_data(
    data_dict=driver_data, table="Drivers",
    cursor=cursor, connection=connection)


# Populate the Restaurants Table
insert_data(
    data_dict=reastaurant_data, table="Restaurants",
    cursor=cursor, connection=connection)


# Populate the MenuItems Table
insert_data(
    data_dict=menu_item_data, table="MenuItems",
    cursor=cursor, connection=connection
)

# Populate the Orders Table
insert_data(
    data_dict=order_data, table="Orders",
    cursor=cursor, connection=connection
)

# Populate the MenuItems Table
insert_data(
    data_dict=delivery_data, table="Deliveries",
    cursor=cursor, connection=connection
)
