-- Create the database if it doesn't exist

CREATE DATABASE IF NOT EXISTS flask_crud_db;


-- Use the newly created database

USE flask_crud_db;


-- Create the users table if it doesn't exist

CREATE TABLE IF NOT EXISTS users (

    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(255) NOT NULL,

    email VARCHAR(255) UNIQUE NOT NULL,

    phone VARCHAR(20)

);


-- Insert some preset data into the users table

-- ON DUPLICATE KEY UPDATE ensures that if you run this multiple times,

-- it won't throw an error for duplicate emails, just updates existing rows.

INSERT INTO users (name, email, phone) VALUES

('John Doe', 'john.doe@example.com', '123-456-7890'),

('Jane Smith', 'jane.smith@example.com', '098-765-4321'),

('Peter Jones', 'peter.jones@example.com', '555-123-4567')

ON DUPLICATE KEY UPDATE name=VALUES(name); -- Example: update name if email exists
