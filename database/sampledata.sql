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
(1, '22B', 'Economy', 950.00),

(2, '2A', 'Economy', 965.00),
(2, '2B', 'Economy', 965.00),
(2, '2C', 'Economy', 965.00),
(2, '2D', 'Economy', 965.00),
(2, '2E', 'Economy', 965.00),
(2, '2F', 'Economy', 965.00),

(3, '7E', 'Economy', 970.00),
(3, '7F', 'Economy', 970.00),
(3, '8E', 'Economy', 970.00),
(3, '8F', 'Economy', 970.00),
(3, '9E', 'Economy', 970.00),
(3, '9F', 'Economy', 970.00),

(4, '4A', 'Economy', 950.00),
(4, '4B', 'Economy', 950.00),
(4, '4C', 'Economy', 950.00),
(4, '4D', 'Economy', 950.00),
(4, '4E', 'Economy', 950.00),
(4, '4F', 'Economy', 950.00),

(5, '5A', 'Economy', 955.00),
(5, '5B', 'Economy', 955.00),
(5, '5C', 'Economy', 955.00),
(5, '5D', 'Economy', 955.00),
(5, '5E', 'Economy', 955.00),
(5, '5F', 'Economy', 955.00),

(6, '6A', 'Economy', 960.00),
(6, '6B', 'Economy', 960.00),
(6, '6C', 'Economy', 960.00),
(6, '6D', 'Economy', 960.00),
(6, '6E', 'Economy', 960.00),
(6, '6F', 'Economy', 960.00),

(7, '7A', 'Economy', 965.00),
(7, '7B', 'Economy', 965.00),
(7, '7C', 'Economy', 965.00),
(7, '7D', 'Economy', 965.00),
(7, '7E', 'Economy', 965.00),
(7, '7F', 'Economy', 965.00),

(8, '8A', 'Economy', 970.00),
(8, '8B', 'Economy', 970.00),
(8, '8C', 'Economy', 970.00),
(8, '8D', 'Economy', 970.00),
(8, '8E', 'Economy', 970.00),
(8, '8F', 'Economy', 970.00),

(9, '9A', 'Economy', 975.00),
(9, '9B', 'Economy', 975.00),
(9, '9C', 'Economy', 975.00),
(9, '9D', 'Economy', 975.00),
(9, '9E', 'Economy', 975.00),
(9, '9F', 'Economy', 975.00),

(10, '10A', 'Economy', 980.00),
(10, '10B', 'Economy', 980.00),
(10, '10C', 'Economy', 980.00),
(10, '10D', 'Economy', 980.00),
(10, '10E', 'Economy', 980.00),
(10, '10F', 'Economy', 980.00),

-- Business Class Seats
(1, '3A', 'Business', 3000.00),
(1, '3B', 'Business', 3000.00),
(1, '3C', 'Business', 3000.00),
(1, '3D', 'Business', 3000.00),

(2, '4A', 'Business', 3100.00),
(2, '4B', 'Business', 3100.00),
(2, '4C', 'Business', 3100.00),
(2, '4D', 'Business', 3100.00),

(3, '5A', 'Business', 3200.00),
(3, '5B', 'Business', 3200.00),
(3, '5C', 'Business', 3200.00),
(3, '5D', 'Business', 3200.00),

(4, '6A', 'Business', 3300.00),
(4, '6B', 'Business', 3300.00),
(4, '6C', 'Business', 3300.00),
(4, '6D', 'Business', 3300.00),

(5, '7A', 'Business', 3400.00),
(5, '7B', 'Business', 3400.00),
(5, '7C', 'Business', 3400.00),
(5, '7D', 'Business', 3400.00),

(6, '8A', 'Business', 3500.00),
(6, '8B', 'Business', 3500.00),
(6, '8C', 'Business', 3500.00),
(6, '8D', 'Business', 3500.00),

(7, '9A', 'Business', 3600.00),
(7, '9B', 'Business', 3600.00),
(7, '9C', 'Business', 3600.00),
(7, '9D', 'Business', 3600.00),

(8, '10A', 'Business', 3700.00),
(8, '10B', 'Business', 3700.00),
(8, '10C', 'Business', 3700.00),
(8, '10D', 'Business', 3700.00),

(9, '11A', 'Business', 3800.00),
(9, '11B', 'Business', 3800.00),
(9, '11C', 'Business', 3800.00),
(9, '11D', 'Business', 3800.00),

(10, '12A', 'Business', 3900.00),
(10, '12B', 'Business', 3900.00),
(10, '12C', 'Business', 3900.00),
(10, '12D', 'Business', 3900.00),

-- First Class Seats
(1, '1A', 'First Class', 5500.00),
(1, '1B', 'First Class', 5500.00),
(1, '1C', 'First Class', 5500.00),

(2, '1A', 'First Class', 5600.00),
(2, '1B', 'First Class', 5600.00),
(2, '1C', 'First Class', 5600.00),

(3, '1A', 'First Class', 5700.00),
(3, '1B', 'First Class', 5700.00),
(3, '1C', 'First Class', 5700.00),

(4, '1A', 'First Class', 5800.00),
(4, '1B', 'First Class', 5800.00),
(4, '1C', 'First Class', 5800.00),

(5, '1A', 'First Class', 5900.00),
(5, '1B', 'First Class', 5900.00),
(5, '1C', 'First Class', 5900.00),

(6, '1A', 'First Class', 6000.00),
(6, '1B', 'First Class', 6000.00),
(6, '1C', 'First Class', 6000.00),

(7, '1A', 'First Class', 6100.00),
(7, '1B', 'First Class', 6100.00),
(7, '1C', 'First Class', 6100.00),

(8, '1A', 'First Class', 6200.00),
(8, '1B', 'First Class', 6200.00),
(8, '1C', 'First Class', 6200.00),

(9, '1A', 'First Class', 6300.00),
(9, '1B', 'First Class', 6300.00),
(9, '1C', 'First Class', 6300.00),

(10, '1A', 'First Class', 6400.00),
(10, '1B', 'First Class', 6400.00),
(10, '1C', 'First Class', 6400.00);



