USE mydb;
CREATE TABLE IF NOT EXISTS `customer` (
  `customer_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `home_lat` DECIMAL(6,5) NOT NULL,
  `home_long` DECIMAL(6,5) NOT NULL,
  PRIMARY KEY (`customer_id`)
  );
CREATE TABLE IF NOT EXISTS `business` (
  `business_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `location_lat` DECIMAL(6,5) NOT NULL,
  `location_long` DECIMAL(6,5) NOT NULL,
  PRIMARY KEY (`business_id`)
  );
  CREATE TABLE IF NOT EXISTS `product` (
  `product_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `price` DECIMAL(3,2) NOT NULL,
  `business_id` INT(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`product_id`),
  CONSTRAINT `business_id`
    FOREIGN KEY (`business_id`)
    REFERENCES `business` (`business_id`)
);
CREATE TABLE IF NOT EXISTS `driver` (
  `driver_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `car_make` VARCHAR(25) NOT NULL,
  `car_colour` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`driver_id`)
  );
CREATE TABLE IF NOT EXISTS `order` (
  `order_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `deliverer_id` INT(10) UNSIGNED NOT NULL,
  `customer_id` INT(10) UNSIGNED NOT NULL,
  `business_id` INT(10) UNSIGNED NOT NULL,
  `product_id` INT(10) UNSIGNED NOT NULL,
  `price` DECIMAL(3,2) NOT NULL,
  `is_complete` TINYINT NOT NULL,
  PRIMARY KEY (`order_id`),
  CONSTRAINT `deliverer_id`
    FOREIGN KEY (`deliverer_id`)
    REFERENCES `driver` (`driver_id`),
  CONSTRAINT `customer_id`
    FOREIGN KEY (`customer_id`)
    REFERENCES `customer` (`customer_id`),
  CONSTRAINT `busness_id`
    FOREIGN KEY (`business_id`)
    REFERENCES `business` (`business_id`),
  CONSTRAINT `product_id`
    FOREIGN KEY (`product_id`)
    REFERENCES `product` (`product_id`)
    );