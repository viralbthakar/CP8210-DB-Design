create_db_query = "CREATE DATABASE IF NOT EXISTS ubereats;"

customer_table_keys = [
    "CustomerID",
    "FirstName",
    "LastName",
    "Email",
    "PhoneNumber",
    "Address",
    "HomeLat",
    "HomeLong"
]
create_customer_table_query = """
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        FirstName VARCHAR(255),
        LastName VARCHAR(255),
        Email VARCHAR(255),
        PhoneNumber VARCHAR(255),
        Address VARCHAR(255),
        HomeLat DECIMAL(6,5) NOT NULL,
        HomeLong DECIMAL(6,5) NOT NULL
    );
"""

reastaurant_table_mapping = {
    "RestaurantID": "id",
    "Name": "name",
    "Score": "score",
    "Ratings": "ratings",
    "Category": "category",
    "PriceRange": "price_range",
    "Address": "full_address",
    "PostalCode": "zip_code",
    "LocationLat": "lat",
    "LocationLong": "lng"
}

create_reastaurant_table_query = """
    CREATE TABLE IF NOT EXISTS Restaurants (
        RestaurantID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255),
        Score FLOAT,
        Ratings INT,
        Category VARCHAR(512),
        PriceRange VARCHAR(255),
        Email VARCHAR(255),
        Address VARCHAR(255),
        PostalCode VARCHAR(255),
        LocationLat FLOAT NOT NULL,
        LocationLong FLOAT NOT NULL
    );
"""

menu_items_table_mapping = {
    "RestaurantID": "restaurant_id",
    "Name": "name",
    "Description": "description",
    "Price": "price"
}

create_menu_items_table_query = """
    CREATE TABLE IF NOT EXISTS MenuItems (
        ItemID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        RestaurantID INT,
        FOREIGN KEY (RestaurantID)
            REFERENCES Restaurants(RestaurantID),
        Name VARCHAR(1024),
        Description VARCHAR(8000),
        Price VARCHAR(255)
    );
"""

create_drivers_table_query = """
    CREATE TABLE IF NOT EXISTS Drivers (
        DriverID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        FirstName VARCHAR(255),
        LastName VARCHAR(255),
        PhoneNumber VARCHAR(255),
        Email VARCHAR(255),
        Address VARCHAR(255)
    );
"""

create_orders_table_query = """
    CREATE TABLE IF NOT EXISTS Orders(
        OrderID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        CustomerID INT NOT NULL,
        FOREIGN KEY(CustomerID)
            REFERENCES Customers(CustomerID),
        RestaurantID INT NOT NULL,
        FOREIGN KEY(RestaurantID)
            REFERENCES Restaurants(RestaurantID),
        ItemID INT NOT NULL,
        FOREIGN KEY(ItemID) REFERENCES MenuItems(ItemID),
        Quantity INT NOT NULL,
        OrderStatus VARCHAR(255),
        OrderDate DATE
    );
"""

create_deliveries_table_query = """
    CREATE TABLE IF NOT EXISTS Deliveries (
        DeliveryID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        OrderID INT NOT NULL,
        FOREIGN KEY (OrderID) 
            REFERENCES Orders(OrderID),
        DriverID INT NOT NULL,
        FOREIGN KEY (DriverID) 
            REFERENCES Drivers(DriverID),
        DeliveryStatus VARCHAR(255),
        DeliveryDate DATE
    );
"""
