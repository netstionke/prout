CREATE DATABASE IF NOT EXISTS jdr;
USE jdr;


CREATE TABLE IF NOT EXISTS users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(25) NOT NULL,
    password VARCHAR(30) NOT NULL, 
    email VARCHAR(150) NOT NULL
);
