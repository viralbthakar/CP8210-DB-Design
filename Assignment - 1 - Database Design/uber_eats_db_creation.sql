USE ubereats;
-- Customers Table
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Email VARCHAR(255),
    PhoneNumber VARCHAR(255),
    Address VARCHAR(255),
    HomeLat DECIMAL(6,5),
    HomeLong DECIMAL(6,5)
);

-- Restaurants Table
CREATE TABLE IF NOT EXISTS Restaurants (
    RestaurantID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    PhoneNumber VARCHAR(255),
    Email VARCHAR(255),
    Address VARCHAR(255),
    LocationLat DECIMAL(6,5),
    LocationLong DECIMAL(6,5)
);

-- Menu Items Table
CREATE TABLE IF NOT EXISTS MenuItems (
    ItemID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    RestaurantID INT,
    FOREIGN KEY (RestaurantID) 
        REFERENCES Restaurants(RestaurantID),
    Name VARCHAR(255),
    Description VARCHAR(255),
    Price DECIMAL(10,2)
);

-- Driver Table
CREATE TABLE IF NOT EXISTS Drivers (
    DriverID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    PhoneNumber VARCHAR(255),
    Email VARCHAR(255),
    Address VARCHAR(255)
);

-- Orders Table
CREATE TABLE IF NOT EXISTS Orders (
    OrderID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    FOREIGN KEY (CustomerID) 
        REFERENCES Customers(CustomerID),
    RestaurantID INT NOT NULL,
    FOREIGN KEY (RestaurantID) 
        REFERENCES Restaurants(RestaurantID),
    DriverID INT NOT NULL,
    FOREIGN KEY (DriverID) 
        REFERENCES Drivers(DriverID),
    ItemID INT NOT NULL,
    FOREIGN KEY (ItemID) REFERENCES MenuItems(ItemID),
    Quantity INT NOT NULL,
    OrderStatus VARCHAR(255),
    OrderDate DATE
);

--Views
--View the menu for a specific restaurant
CREATE VIEW Menu AS
	SELECT MenuItems.ItemID, MenuItems.Name
    FROM MenuItems, Restaurants WHERE
    Restaurants.Name = "McDonald's"
    Restaurants.RestaurantID = MenuItems.RestaurantID;

--Use haversine distance to find restaurants within 
--a 5 kilometer radius of the user
CREATE VIEW Within5KM AS
	SELECT Restaurants.RestaurantID, Restaurants.Name,
    acos(cos(radians( Customers.HomeLat ))* 
    cos(radians( Restaurants.LocationLat ))* 
    cos(radians( Customers.HomeLong ) - 
    radians( Restaurants.LocationLong ))+ 
    sin(radians( Customers.HomeLat )) * 
    sin(radians( Restaurants.LocationLat ))) as haversine
    FROM Restaurants, Customers WHERE
    haversine < 5
    ORDER BY haversine;

 
--Functions/Procedures
DELIMETER //
--Create Customer Profile
CREATE PROCEDURE createCustomerProfile (IN FirstName VARCHAR(255), IN LastName VARCHAR(255), IN Email VARCHAR(255), IN PhoneNumber VARCHAR(255), IN Address VARCHAR(255) )
       BEGIN
         INSERT INTO Customers(FirstName, LastName, Email, PhoneNumber, Address)
       END//
--Create Driver Profile
CREATE PROCEDURE createDriverProfile (IN FirstName VARCHAR(255), IN LastName VARCHAR(255), IN Email VARCHAR(255), IN PhoneNumber VARCHAR(255), IN Address VARCHAR(255) )
       BEGIN
         INSERT INTO Drivers(FirstName, LastName, Email, PhoneNumber, Address)
       END//
--Create Business Profile
CREATE PROCEDURE createBusinessProfile (IN Name VARCHAR(255), IN Email VARCHAR(255), IN PhoneNumber VARCHAR(255), IN Address VARCHAR(255) )
       BEGIN
         INSERT INTO Restaurants(FirstName, LastName, Email, PhoneNumber, Address)
       END//
--Add Items to menu
--Create Driver Profile
CREATE PROCEDURE createDriverProfile (IN FirstName VARCHAR(255), IN LastName VARCHAR(255), IN Email VARCHAR(255), IN PhoneNumber VARCHAR(255), IN Address VARCHAR(255) )
       BEGIN
         INSERT INTO Drivers(FirstName, LastName, Email, PhoneNumber, Address)
       END//
--Dummy Function to find Latitude and Longitude based on address
CREATE PROCEDURE geoCodeAddress (IN Address VARCHAR(255), OUT Latitude DECIMAL(6,5),OUT Longitude DECIMAL(6,5))
       BEGIN
         INSERT INTO Customers(FirstName, LastName, Email, PhoneNumber, Address)
       END//
DELIMETER ;

-- Delivery Table
-- CREATE TABLE Deliveries (
--     DeliveryID INT PRIMARY KEY,
--     OrderID INT,
--     FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
--     DriverID INT,
--     FOREIGN KEY (DriverID) REFERENCES Drivers(DriverID),
--     DeliveryStatus VARCHAR(255),
--     DeliveryDate DATE
-- );
