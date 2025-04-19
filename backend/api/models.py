from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None, date_of_birth=None, phone_number=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, first_name=None, last_name=None, date_of_birth=None, phone_number=None, **extra_fields):
      extra_fields.setdefault('is_admin', True)
      extra_fields.setdefault('is_staff', True)
      user = self.create_user(email, password, first_name, last_name, date_of_birth, phone_number, **extra_fields)
      Admin.objects.create(AdminID=user) # add superuser to the Admin table once created
      return user

class FlightManager(models.Manager):
  # Method to return flights based on the departure and arrival airports
  def get_flights_by_airports(self, departure_airport=None, arrival_airport=None):
    return self.filter(departure_airport=departure_airport, arrival_airport=arrival_airport)
  
class SeatManager(models.Manager):
  # Method to return seats based on the Seat Class
  def get_available_seats(self, flight_id=None, class_type=None):
    booked_seats = BookingSeat.objects.values_list('seat_id', flat=True) # get all the seats that are already booked/reserved
    available_seats =  self.exclude(SeatID__in=booked_seats)              # get all seats that are available
    return available_seats.filter(FlightID=flight_id, Class=class_type)
    
class User(AbstractBaseUser):
    UserID = models.AutoField(primary_key=True, db_column='UserID')
    first_name = models.CharField(max_length=50, db_column='FirstName')
    last_name = models.CharField(max_length=50, db_column='LastName')
    date_of_birth = models.DateField(null=True, blank=True, db_column='DateOfBirth')
    phone_number = models.CharField(max_length=15, blank=True, db_column='PhoneNumber')
    email = models.EmailField(unique=True, db_column='Email')
    password = models.CharField(max_length=128, db_column='Password')
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    last_login = None
    # is_active = None
    # is_admin = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        managed = False
        db_table = 'User'

    def has_perm(self, api):
      return self.is_admin
    
    def has_module_perms(self, api):
      return self.is_admin
    
    def set_password(self, raw_password):
        self.password = raw_password
        self.save()

    def check_password(self, raw_password):
        return self.password == raw_password

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Admin(models.Model):
    AUTHORIZATION_LEVEL_CHOICES = [
      ('SuperAdmin', 'SuperAdmin'),
      ('GeneralAdmin', 'GeneralAdmin'),
      ('CustomerSupport', 'CustomerSupport')
    ]
    
    AdminID = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='AdminID'
    )
    authorization_level = models.CharField(max_length=50, default="GeneralAdmin", db_column="AuthorizationLevel") # link to MySQL database

    class Meta:
        managed = False
        db_table = 'Admin'

class Passenger(models.Model):
    PassengerID = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='PassengerID'
    )
    PassportNumber = models.CharField(
        max_length=20, 
        unique=True, 
        null=True, 
        blank=True
    )
    LoyaltyNumber = models.CharField(
        max_length=20, 
        unique=True, 
        null=True, 
        blank=True
    )
    Status = models.CharField(
        max_length=20, 
        default="Active"
    )

    class Meta:
        managed = False
        db_table = 'Passenger'

class Aircraft(models.Model):
    aircraft_id = models.AutoField(primary_key=True, db_column="AircraftID")
    model = models.CharField(max_length=50, db_column="Model")
    capacity = models.IntegerField(db_column="Capacity")

    class Meta:
        managed = False
        db_table = 'Aircraft'

class Flight(models.Model):
    flight_id = models.AutoField(primary_key=True, db_column="FlightID")
    flight_number = models.CharField(max_length=10, unique=True, db_column="FlightNumber")
    departure_airport = models.CharField(max_length=50, db_column="DepartureAirport")
    arrival_airport = models.CharField(max_length=50, db_column="ArrivalAirport")
    departure_time = models.DateTimeField(db_column="DepartureTime")
    arrival_time = models.DateTimeField(db_column="ArrivalTime")
    aircraft_id = models.ForeignKey(Aircraft, models.CASCADE, db_column='AircraftID')
    
    objects = FlightManager()    # Assign to custom FlightManager

    class Meta:
        managed = False
        db_table = 'Flight'

class Booking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
    ]
    
    booking_id = models.AutoField(primary_key=True, db_column='BookingID')
    passenger_id= models.ForeignKey(Passenger, models.CASCADE, db_column='PassengerID')
    flight_id = models.ForeignKey(Flight, models.CASCADE, db_column='FlightID')
    booking_date = models.DateTimeField(auto_now_add=True, db_column='BookingDate')
    booking_status = models.CharField(max_length=10, choices=BOOKING_STATUS_CHOICES, db_column='BookingStatus')
    admin_id = models.ForeignKey(Admin, models.SET_NULL, null=True, blank=True, db_column='AdminID')
    
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
    
    objects = SeatManager()

    class Meta:
        managed = False
        db_table = 'Seat'

class BookingSeat(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE, db_column='BookingID')
    seat_id = models.ForeignKey(Seat, models.CASCADE, db_column='SeatID')

    class Meta:
        managed = False
        db_table = 'BookingSeat'
        unique_together = (('booking_id', 'seat_id'),)

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