
-- Create the Airline Booking System Database with checks and settings
CREATE DATABASE IF NOT EXISTS AirlineBookingSystem
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;

-- Use the database
USE AirlineBookingSystem;

-- User Table (General users: Passengers & Admins)
CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    DateOfBirth DATE,
    PhoneNumber VARCHAR(15),
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(256) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    is_staff BOOLEAN DEFAULT FALSE
);

-- Admin Table (Specialized user role)
CREATE TABLE Admin (
    AdminID INT PRIMARY KEY,
    AuthorizationLevel VARCHAR(50) NOT NULL,
    FOREIGN KEY (AdminID) REFERENCES User(UserID) ON DELETE CASCADE
);

-- Passenger Table (Specialized user role)
CREATE TABLE Passenger (
    PassengerID INT PRIMARY KEY,
    PassportNumber VARCHAR(20) UNIQUE,
    LoyaltyNumber VARCHAR(20) UNIQUE,
    Status VARCHAR(20), -- e.g., "Active", "Blacklisted"
    FOREIGN KEY (PassengerID) REFERENCES User(UserID) ON DELETE CASCADE
);

-- Aircraft Table (Each Flight is Operated by an Aircraft)
CREATE TABLE Aircraft (
    AircraftID INT AUTO_INCREMENT PRIMARY KEY,
    Model VARCHAR(50) NOT NULL,
    Capacity INT NOT NULL
);

-- Flight Table (Stores Flight Information)
CREATE TABLE Flight (
    FlightID INT AUTO_INCREMENT PRIMARY KEY,
    FlightNumber VARCHAR(10) UNIQUE NOT NULL,
    DepartureAirport VARCHAR(50) NOT NULL,
    ArrivalAirport VARCHAR(50) NOT NULL,
    DepartureTime DATETIME NOT NULL,
    ArrivalTime DATETIME NOT NULL,
    AircraftID INT NOT NULL,
    CHECK (ArrivalTime > DepartureTime),
    FOREIGN KEY (AircraftID) REFERENCES Aircraft(AircraftID) ON DELETE CASCADE
);

-- Booking Table (The Link from Passengers to Flights)
CREATE TABLE Booking (
    BookingID INT AUTO_INCREMENT PRIMARY KEY,
    PassengerID INT NOT NULL,
    FlightID INT NOT NULL,
    BookingDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    BookingStatus ENUM('Confirmed', 'Pending', 'Cancelled') NOT NULL,
    AdminID INT NULL, -- Optional: Admin managing the booking
    FOREIGN KEY (PassengerID) REFERENCES Passenger(PassengerID) ON DELETE CASCADE,
    FOREIGN KEY (FlightID) REFERENCES Flight(FlightID) ON DELETE CASCADE,
    FOREIGN KEY (AdminID) REFERENCES Admin(AdminID) ON DELETE SET NULL
);

-- Seat Table (Tracks all seats available on a flight)
CREATE TABLE Seat (
    SeatID INT AUTO_INCREMENT PRIMARY KEY,
    FlightID INT NOT NULL,
    SeatNumber VARCHAR(10) NOT NULL,
    Class ENUM('Economy', 'Business', 'First Class') NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (FlightID) REFERENCES Flight(FlightID) ON DELETE CASCADE
);

-- BookingSeat Table (Handles Many-to-Many Relationship: One Booking Can Reserve Multiple Seats)
CREATE TABLE BookingSeat (
    BookingID INT NOT NULL,
    SeatID INT NOT NULL,
    PRIMARY KEY (BookingID, SeatID),
    FOREIGN KEY (BookingID) REFERENCES Booking(BookingID) ON DELETE CASCADE,
    FOREIGN KEY (SeatID) REFERENCES Seat(SeatID) ON DELETE CASCADE
);

-- Ticket Table (A Weak Entity Identified by BookingID + SequenceNumber)
CREATE TABLE Ticket (
    TicketID INT AUTO_INCREMENT PRIMARY KEY,
    BookingID INT NOT NULL,
    SequenceNumber INT NOT NULL,
    BoardingGroup VARCHAR(10),
    CheckInStatus ENUM('Checked In', 'Not Checked In') NOT NULL,
    FOREIGN KEY (BookingID) REFERENCES Booking(BookingID) ON DELETE CASCADE,
    UNIQUE (BookingID, SequenceNumber) -- Ensures uniqueness as a weak entity
);

-- CheckIn Table (Tracks passengers checking into flights)
CREATE TABLE CheckIn (
    CheckInID INT AUTO_INCREMENT PRIMARY KEY,
    PassengerID INT NOT NULL,
    FlightID INT NOT NULL,
    CheckInStatus ENUM('Checked In', 'Not Checked In') NOT NULL,
    FOREIGN KEY (PassengerID) REFERENCES Passenger(PassengerID) ON DELETE CASCADE,
    FOREIGN KEY (FlightID) REFERENCES Flight(FlightID) ON DELETE CASCADE
);

-- Payment Table (Handles Payments for Bookings)
CREATE TABLE Payment (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    BookingID INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (BookingID) REFERENCES Booking(BookingID) ON DELETE CASCADE
);