USE ubereats;
-- Customers Table
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Email VARCHAR(255),
    PhoneNumber VARCHAR(255),
    Address VARCHAR(255),
    HomeLat FLOAT NOT NULL,
    HomeLong FLOAT NOT NULL
);

-- Restaurants Table
CREATE TABLE IF NOT EXISTS Restaurants (
    RestaurantID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Score FLOAT,
    Ratings INT,
    Category VARCHAR(512),
    PriceRange VARCHAR(255),
    PhoneNumber VARCHAR(255),
    Email VARCHAR(255),
    Address VARCHAR(255),
    PostalCode VARCHAR(255),
    LocationLat FLOAT NOT NULL,
    LocationLong FLOAT NOT NULL
);

-- Menu Items Table
CREATE TABLE IF NOT EXISTS MenuItems (
    ItemID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    RestaurantID INT,
    FOREIGN KEY (RestaurantID)
            REFERENCES Restaurants(RestaurantID),
    Name VARCHAR(1024),
    Description VARCHAR(8000),
    Price VARCHAR(255)
);

-- Driver Table
CREATE TABLE IF NOT EXISTS Drivers (
    DriverID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    PhoneNumber VARCHAR(255),
    Email VARCHAR(255),
    Address VARCHAR(255),
    HomeLat FLOAT NOT NULL,
    HomeLong FLOAT NOT NULL
);

-- Orders Table
CREATE TABLE IF NOT EXISTS Orders (
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

-- Delivery Table
CREATE TABLE Deliveries (
    DeliveryID INT PRIMARY KEY,
    OrderID INT,
    FOREIGN KEY (OrderID) 
        REFERENCES Orders(OrderID),
    DriverID INT,
    FOREIGN KEY (DriverID) 
        REFERENCES Drivers(DriverID),
    DeliveryStatus VARCHAR(255),
    DeliveryDate DATE
);

--Views
--View the menu for a specific restaurant
CREATE VIEW Menu AS
	SELECT MenuItems.ItemID, MenuItems.Name
    FROM MenuItems, Restaurants WHERE
    Restaurants.Name = "Chipotle Mexican Grill (1821 Cherokee Ave SW)";

--Use haversine distance to find restaurants within 
--a 5 kilometer radius of the user
CREATE VIEW Within50km AS
SELECT Restaurants.RestaurantID, Restaurants.Name,
       ( 6371 * acos( cos( radians(Customers.HomeLat) ) * 
                      cos( radians( Restaurants.LocationLat ) ) * 
                      cos( radians( Restaurants.LocationLong ) - 
                           radians(Customers.HomeLong) ) + 
                      sin( radians(Customers.HomeLat) ) * 
                      sin( radians( Restaurants.LocationLat ) ) ) ) AS distance 
FROM Restaurants, Customers 
HAVING distance < 50 
ORDER BY distance;

 
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


