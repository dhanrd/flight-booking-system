-- Insert Users
INSERT INTO User (FirstName, LastName, DateOfBirth, PhoneNumber, Email) 
VALUES 
('John', 'Doe', '1990-05-15', '123-456-7890', 'johndoe@email.com'),
('Alice', 'Smith', '1985-09-25', '987-654-3210', 'alicesmith@email.com');

-- Select all columns from a table
SELECT * FROM table_name;

-- Select specific columns with a condition
SELECT column1, column2 FROM table_name WHERE column3 = 'some_value';

-- Count the number of records in a table
SELECT COUNT(*) FROM table_name;

-- Select data sorted by a column
SELECT column1, column2 FROM table_name ORDER BY column1 DESC;

-- Update a specific column for certain records
UPDATE table_name 
SET column1 = 'new_value' 
WHERE column2 = 'some_condition';

-- Update multiple columns at once
UPDATE table_name 
SET column1 = 'new_value', column2 = 'another_value' 
WHERE column3 > 100;

-- Delete specific records based on a condition
DELETE FROM table_name WHERE column1 = 'some_value';

-- Delete all records from a table (use with caution!)
DELETE FROM table_name;

-- Delete records that meet multiple conditions
DELETE FROM table_name WHERE column1 = 'value1' AND column2 < 50;