from rest_framework import serializers
from .models import Booking, Flight, Ticket, User, Passenger, Admin, Seat, BookingSeat, Payment, CheckIn

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['UserID', 'email', 'password', 'first_name', 'last_name', 
                 'date_of_birth', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
            'UserID': {'read_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data.get('date_of_birth'),
            phone_number=validated_data.get('phone_number')
        )
        return user

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['PassengerID', 'PassportNumber', 'LoyaltyNumber', 'Status']
        extra_kwargs = {
            'PassportNumber': {'required': False},
            'LoyaltyNumber': {'required': False},
            'Status': {'required': False}
        }

    def create(self, validated_data):
        # Extract user data if present
        user_data = validated_data.pop('user', None)
        
        # Create passenger record
        passenger = Passenger.objects.using('default').create(**validated_data)
        return passenger

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Admin
        fields = ['user', 'authorization_level']
        
class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
      model = Seat
      fields = '__all__'
    
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        
    # Create Booking record 
    def create(self, validated_data):
      booking = Booking.objects.create(**validated_data)
      return booking

class BookingSeatSerializer(serializers.ModelSerializer):
    class Meta:
      model = BookingSeat
      fields = ['booking_id', 'seat_id']
      
    # Create BookingSeat record
    def create(self, validated_data):
      booking_seat = BookingSeat.objects.create(**validated_data)
      return booking_seat
  
class PaymentSerializer(serializers.ModelSerializer):
  class Meta: 
    model = Payment
    fields = '__all__'    
    
    # Create Payment record
    def create(self, validated_data):
      payment = Payment.objects.create(**validated_data)
      return payment
    
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
    
    # Create Ticket record
    def create(self, validated_data):
      ticket = Ticket.objects.create(**validated_data)
      return ticket

class CheckInSerializer(serializers.ModelSerializer):
  class Meta:
    model = CheckIn
    fields = '__all__'
    
  def create(self, validated_data):
    checkInRecord = CheckIn.objects.create(**validated_data)
    return checkInRecord