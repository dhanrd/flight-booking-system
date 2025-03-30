# api/models.py
from django.db import models

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    DateOfBirth = models.DateField(null=True, blank=True)
    PhoneNumber = models.CharField(max_length=15, null=True, blank=True)
    Email = models.EmailField(max_length=100, unique=True)

    class Meta:
        managed = False
        db_table = 'User'

class Admin(models.Model):
    AdminID = models.OneToOneField(User, models.CASCADE, primary_key=True, db_column='AdminID')
    AuthorizationLevel = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'Admin'

class Passenger(models.Model):
    PassengerID = models.OneToOneField(User, models.CASCADE, primary_key=True, db_column='PassengerID')
    PassportNumber = models.CharField(max_length=20, unique=True, null=True, blank=True)
    LoyaltyNumber = models.CharField(max_length=20, unique=True, null=True, blank=True)
    Status = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Passenger'

class Aircraft(models.Model):
    AircraftID = models.AutoField(primary_key=True)
    Model = models.CharField(max_length=50)
    Capacity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Aircraft'

class Flight(models.Model):
    FlightID = models.AutoField(primary_key=True)
    FlightNumber = models.CharField(max_length=10, unique=True)
    DepartureAirport = models.CharField(max_length=50)
    ArrivalAirport = models.CharField(max_length=50)
    DepartureTime = models.DateTimeField()
    ArrivalTime = models.DateTimeField()
    AircraftID = models.ForeignKey(Aircraft, models.CASCADE, db_column='AircraftID')

    class Meta:
        managed = False
        db_table = 'Flight'

class Booking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
    ]
    
    BookingID = models.AutoField(primary_key=True)
    PassengerID = models.ForeignKey(Passenger, models.CASCADE, db_column='PassengerID')
    FlightID = models.ForeignKey(Flight, models.CASCADE, db_column='FlightID')
    BookingDate = models.DateTimeField(auto_now_add=True)
    BookingStatus = models.CharField(max_length=10, choices=BOOKING_STATUS_CHOICES)
    AdminID = models.ForeignKey(Admin, models.SET_NULL, null=True, blank=True, db_column='AdminID')

    class Meta:
        managed = False
        db_table = 'Booking'

class Seat(models.Model):
    SEAT_CLASS_CHOICES = [
        ('Economy', 'Economy'),
        ('Business', 'Business'),
        ('First Class', 'First Class'),
    ]
    
    SeatID = models.AutoField(primary_key=True)
    FlightID = models.ForeignKey(Flight, models.CASCADE, db_column='FlightID')
    SeatNumber = models.CharField(max_length=10)
    Class = models.CharField(max_length=15, choices=SEAT_CLASS_CHOICES)
    Price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'Seat'

class BookingSeat(models.Model):
    BookingID = models.OneToOneField(Booking, models.CASCADE, primary_key=True, db_column='BookingID')
    SeatID = models.ForeignKey(Seat, models.CASCADE, db_column='SeatID')

    class Meta:
        managed = False
        db_table = 'BookingSeat'
        unique_together = (('BookingID', 'SeatID'),)

class Ticket(models.Model):
    CHECK_IN_STATUS_CHOICES = [
        ('Checked In', 'Checked In'),
        ('Not Checked In', 'Not Checked In'),
    ]
    
    TicketID = models.AutoField(primary_key=True)
    BookingID = models.ForeignKey(Booking, models.CASCADE, db_column='BookingID')
    SequenceNumber = models.IntegerField()
    BoardingGroup = models.CharField(max_length=10, null=True, blank=True)
    CheckInStatus = models.CharField(max_length=15, choices=CHECK_IN_STATUS_CHOICES)
    
    class Meta:
        managed = False
        db_table = 'Ticket'
        unique_together = (('BookingID', 'SequenceNumber'),)

class CheckIn(models.Model):
    CHECK_IN_STATUS_CHOICES = [
        ('Checked In', 'Checked In'),
        ('Not Checked In', 'Not Checked In'),
    ]
    
    CheckInID = models.AutoField(primary_key=True)
    PassengerID = models.ForeignKey(Passenger, models.CASCADE, db_column='PassengerID')
    FlightID = models.ForeignKey(Flight, models.CASCADE, db_column='FlightID')
    CheckInStatus = models.CharField(max_length=15, choices=CHECK_IN_STATUS_CHOICES)

    class Meta:
        managed = False
        db_table = 'CheckIn'

class Payment(models.Model):
    PaymentID = models.AutoField(primary_key=True)
    BookingID = models.ForeignKey(Booking, models.CASCADE, db_column='BookingID')
    Amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'Payment'