import os
import kaggle
import pandas as pd
from getpass import getpass
from mysql.connector import connect, Error
from utils import execute_and_commit, fetch_data, styled_print

database_name = 'ubereats'
rows_to_print = 10

# Connect to Database
styled_print(
    text=f"Connecting to Database `{database_name}`", header=True)
try:
    connection = connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database="ubereats"
    )
    cursor = connection.cursor(buffered=True)
except Error as e:
    print(e)

connection.cmd_query('SET GLOBAL connect_timeout=28800')
connection.cmd_query('SET GLOBAL interactive_timeout=28800')
connection.cmd_query('SET GLOBAL wait_timeout=28800')


# View the menu for a specific restaurant.
restaurant_name = "PJ Fresh (224 Daniel Payne Drive)"
menu_name = 'my_menu'
styled_print(f"Creating View `{menu_name}` for `{restaurant_name}`", True)

all_exiting_views = dict(fetch_data(
    f"""SHOW FULL TABLES IN {database_name}  WHERE TABLE_TYPE LIKE 'VIEW';""", cursor))
styled_print(f"Found `{all_exiting_views}` existing views", False)

if len(all_exiting_views) >= 1 and menu_name in all_exiting_views.keys():
    styled_print(text=f"View `{menu_name}` Exists ", header=False)
    # execute_and_commit(f"""DROP VIEW `{menu_name}`;""", connection, cursor)
else:
    styled_print(text=f"Creating View `{menu_name}` ", header=False)
    query = f"""CREATE VIEW {menu_name} AS
                    SELECT MenuItems.Name AS ItemName, MenuItems.Price, MenuItems.Description, Restaurants.Name
                    From Restaurants
                    INNER JOIN MenuItems ON Restaurants.RestaurantID = MenuItems.RestaurantID
                    WHERE Restaurants.Name = '{restaurant_name}';"""
    execute_and_commit(query, connection, cursor)

df = fetch_data(
    f"""SELECT * FROM {database_name}.{menu_name};""", cursor, size=None, as_df=True)
print(df.head(rows_to_print))


# Use haversine distance to find restaurants within.
distance = 50
view_name = f"within{distance}km"
styled_print(f"Creating View for Restaurants Within {distance}km", header=True)
all_exiting_views = dict(fetch_data(
    f"""SHOW FULL TABLES IN {database_name}  WHERE TABLE_TYPE LIKE 'VIEW';""", cursor))
styled_print(f"Found `{all_exiting_views}` existing views", False)

if len(all_exiting_views) >= 1 and view_name in all_exiting_views.keys():
    styled_print(text=f"View `{view_name}` Exists", header=False)
    # execute_and_commit(f"""DROP VIEW `{view_name}`;""", connection, cursor)
else:
    styled_print(text=f"Creating View `{view_name}` ", header=False)
    query = f"""CREATE VIEW {view_name} AS
                    SELECT Customers.CustomerID, Customers.FirstName, Restaurants.RestaurantID, Restaurants.Name, Restaurants.Address,
                        ( 6371 * acos(cos(radians(Customers.HomeLat)) *
                                        cos(radians(Restaurants.LocationLat)) *
                                        cos(radians( Restaurants.LocationLong) -
                                            radians(Customers.HomeLong)) +
                                        sin(radians(Customers.HomeLat)) *
                                        sin(radians(Restaurants.LocationLat)))) AS distance
                    FROM Restaurants, Customers
                    HAVING distance < {distance}
                    ORDER BY distance;
    """
    execute_and_commit(query, connection, cursor)
df = fetch_data(
    f"""SELECT * FROM {database_name}.{view_name};""", cursor, size=50, as_df=True)
print(df.head(rows_to_print))


# Query to select all the Restaurants.
styled_print(f"Executing Query to Select All the Restaurants", header=True)
query = "SELECT * FROM Restaurants;"
df = fetch_data(query, cursor, size=None, as_df=True)
print(df.head(rows_to_print))

# Query to display the delivery details of all deliveries made in the last month.
months = 1
styled_print(
    f"Query to display the delivery details of all deliveries made in the last {months} month/months.", header=True)
query = f"""SELECT * FROM Deliveries 
            WHERE Deliveries.DeliveryDate BETWEEN DATE_SUB(NOW(), INTERVAL {months} MONTH) AND NOW();
        """
df = fetch_data(query, cursor, size=None, as_df=True)
print(df.head(rows_to_print))

# Query to display the average order quantity for each restaurant.
styled_print(
    f"Query to display the average order quantity for each restaurant.", header=True)
query = f"""SELECT Orders.RestaurantID, AVG(Orders.Quantity) AS avg_order_quantity 
            FROM Orders 
            GROUP BY RestaurantID;
        """
df = fetch_data(query, cursor, size=None, as_df=True)
print(df.head(rows_to_print))

# Query to display all the deliveries done by a specific driver.
driver_id = 2
styled_print(
    f"Query to display all the deliveries done by a specific driver {driver_id}.", header=True)
query = f"""SELECT * FROM Deliveries 
            WHERE DriverID = {driver_id};
        """
df = fetch_data(query, cursor, size=None, as_df=True)
print(df.head(rows_to_print))

# Query to display the total number of deliveries made by each driver.
styled_print(
    f"Query to display the total number of deliveries made by each driver.", header=True)
query = f"""SELECT DriverID, COUNT(DeliveryID) AS deliveries_count 
            FROM Deliveries
            GROUP BY DriverID;
        """
df = fetch_data(query, cursor, size=None, as_df=True)
print(df.head(rows_to_print))

# Query to get the most ordered item for each restaurant.
styled_print(
    "Query to get the most ordered item for each restaurant.", header=True)
query = """SELECT Restaurants.Name, MenuItems.Name, COUNT(Orders.OrderID) as total_orders
            FROM Restaurants
            JOIN Orders ON Restaurants.RestaurantID = Orders.RestaurantID
            JOIN MenuItems ON Orders.ItemID = MenuItems.ItemID
            GROUP BY Restaurants.Name, MenuItems.Name
            ORDER BY total_orders DESC;
        """
df = fetch_data(query, cursor, size=None, as_df=True)
print(df.head(rows_to_print))
