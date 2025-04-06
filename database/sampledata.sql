-- Insert Users
INSERT INTO User (FirstName, LastName, DateOfBirth, PhoneNumber, Email, Password) 
VALUES 
('John', 'Doe', '1990-05-15', '123-456-7890', 'johndoe@email.com', 'pizzalover123'),
('Alice', 'Smith', '1985-09-25', '987-654-3210', 'alicesmith@email.com', 'bluesky#789');

-- Insert Aircrafts
INSERT INTO Aircraft (Model, Capacity)
VALUES
('Boeing 737-800', 174),
('Airbus A320neo', 180),
('Embraer E190', 100),
('Boeing 777-300ER', 396),
('Airbus A350-900', 325);

-- Insert Flights
INSERT INTO Flight (FlightNumber, DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, AircraftID)
VALUES
('AC101', 'YYC', 'YVR', '2025-04-07 08:00:00-06:00', '2025-04-07 09:15:00-07:00', 1), -- Calgary to Vancouver 
('WS117', 'YYC', 'YVR', '2025-04-07 14:00:00-06:00', '2025-04-07 15:15:00-07:00', 2), -- Calgary to Vancouver
('AC401', 'YYZ', 'YUL', '2025-04-08 07:00:00-04:00', '2025-04-08 08:10:00-04:00', 3), -- Toronto to Montreal
('WS605', 'YYZ', 'YUL', '2025-04-08 09:00:00-04:00', '2025-04-08 10:10:00-04:00', 4), -- Toronto to Montreal
('QF012', 'LAX', 'SYD', '2025-04-11 22:00:00-07:00', '2025-04-13 06:30:00+10:00', 5), -- Los Angeles to Sydney
('QF018', 'LAX', 'SYD', '2025-04-12 10:00:00-07:00', '2025-04-13 18:30:00+10:00', 1), -- Los Angeles to Sydeny
('WS150', 'YYC', 'LAX', '2025-04-06 15:00:00-06:00', '2025-04-06 17:00:00-07:00', 2), -- Calgary to Los Angeles
('BA117', 'LHR', 'JFK', '2025-04-09 11:00:00+01:00', '2025-04-09 14:00:00-04:00', 3), -- London to New York
('JL005', 'HND', 'SYD', '2025-04-12 20:00:00+09:00', '2025-04-13 06:00:00+10:00', 4), -- Tokyo to Sydney
('AF006', 'CDG', 'YYC', '2025-04-10 16:00:00+02:00', '2025-04-11 18:00:00-06:00', 5); -- Paris to Calgary

-- Insert Seats for FlightID 1
INSERT INTO Seat (FlightID, SeatNumber, Class, Price)
VALUES 

-- Economy Class Seats
(1, '20A', 'Economy', 950.00),
(1, '20B', 'Economy', 950.00),
(1, '21A', 'Economy', 950.00),
(1, '21B', 'Economy', 950.00),
(1, '22A', 'Economy', 950.00),


-- Business Class Seats
(1, '3A', 'Business', 3200.00),
(1, '3B', 'Business', 3200.00),
(1, '4A', 'Business', 3200.00),
(1, '4B', 'Business', 3200.00),

-- First Class Seats
(1, '1A', 'First', 5500.00),
(1, '1B', 'First', 5500.00),
(1, '2A', 'First', 5500.00);


