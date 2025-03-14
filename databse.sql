-- =============================================================================
-- DATABASE CREATION
-- =============================================================================
CREATE DATABASE IF NOT EXISTS sms;
USE sms;

-- =============================================================================
-- USER REGISTRATION TABLE (signup)
-- =============================================================================
CREATE TABLE IF NOT EXISTS signup (
    username VARCHAR(255) NOT NULL,
    mobile VARCHAR(15) NOT NULL,
    email VARCHAR(255) PRIMARY KEY,
    address TEXT NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- =============================================================================
-- STUDENTS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- =============================================================================
-- SAMPLE DATA (Optional)
-- =============================================================================
-- Sample user for login testing
INSERT INTO signup (username, mobile, email, address, password) 
VALUES ('Test User', '1234567890', 'test@example.com', '123 Main St', 'testpassword');

-- Sample student data
INSERT INTO students (name, address, age, email)
VALUES ('John Doe', '456 Oak Avenue', 20, 'john@example.com'),
       ('Jane Smith', '789 Pine Road', 22, 'jane@example.com');



/*

Key features of this schema:
    1. Creates sms database if not exists
    2. Creates two tables:
        - signup: Stores user registration details with email as primary key
        - students: Stores student records with auto-incrementing ID as primary key
    3. Includes sample data for testing
    4. Matches the field names and structure used in your Flask routes
        
*/