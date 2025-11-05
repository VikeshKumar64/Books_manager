-- Create and use your database
CREATE DATABASE IF NOT EXISTS vikeshdb;
USE vikeshdb;

-- Books table
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    copies INT
);

-- Users table (login)
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50)
);

-- Students table
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    roll_no VARCHAR(50)
);

-- Issued books table
CREATE TABLE IF NOT EXISTS issued_books (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    book_id INT,
    issue_date DATE,
    return_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
);

-- Insert default login user
INSERT IGNORE INTO users (username, password) VALUES ('Vikesh', '12345');


