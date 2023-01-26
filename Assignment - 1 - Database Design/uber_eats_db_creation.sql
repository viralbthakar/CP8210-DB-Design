USE ubereats;
-- Customers Table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Email VARCHAR(255),
    PhoneNumber VARCHAR(255),
    Address VARCHAR(255)
);

-- Restaurants Table
CREATE TABLE Restaurants (
    RestaurantID INT PRIMARY KEY,
    Name VARCHAR(255),
    PhoneNumber VARCHAR(255),
    Email VARCHAR(255),
    Address VARCHAR(255)
);

-- Menu Items Table
CREATE TABLE MenuItems (
    ItemID INT PRIMARY KEY,
    RestaurantID INT,
    FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID),
    Name VARCHAR(255),
    Description VARCHAR(255),
    Price DECIMAL(10,2)
);

-- Orders Table
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    RestaurantID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID),
    ItemID INT,
    FOREIGN KEY (ItemID) REFERENCES MenuItems(ItemID),
    Quantity INT,
    OrderStatus VARCHAR(255),
    OrderDate DATE
);

-- Driver Table
CREATE TABLE Drivers (
    DriverID INT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    PhoneNumber VARCHAR(255),
    Email VARCHAR(255),
    Address VARCHAR(255)
);

-- Delivery Table
CREATE TABLE Deliveries (
    DeliveryID INT PRIMARY KEY,
    OrderID INT,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    DriverID INT,
    FOREIGN KEY (DriverID) REFERENCES Drivers(DriverID),
    DeliveryStatus VARCHAR(255),
    DeliveryDate DATE
);
