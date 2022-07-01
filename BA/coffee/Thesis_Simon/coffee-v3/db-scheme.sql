SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;

DROP DATABASE IF EXISTS coffee;
CREATE DATABASE coffee
DEFAULT CHARACTER SET utf8mb4;

USE coffee;

CREATE TABLE users (
  id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  token varchar(20) NOT NULL,
  name varchar(45) NOT NULL,
  balance int(11) NOT NULL,
  coffee_milk_pref tinyint(1),
  water_milk_pref tinyint(1),
  UNIQUE KEY token_UNIQUE(token)
) ENGINE=InnoDB;

CREATE TABLE uids (
  uid varchar(20) NOT NULL PRIMARY KEY,
  user_id int(11) NOT NULL,
  FOREIGN KEY fk_uids(user_id)
  REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE orders (
  id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  uid varchar(20) NOT NULL,
  coffee tinyint(1) NOT NULL,
  milk tinyint(1) NOT NULL,
  price int(11) NOT NULL,
  cheated tinyint(1) NOT NULL,
  is_synchronized tinyint(1) NOT NULL DEFAULT false,
  FOREIGN KEY fk_orders(uid)
  REFERENCES uids(uid)
) ENGINE=InnoDB;
COMMIT;