from rest_framework import serializers
from .models import Booking, Flight, Ticket, User, Passenger, Admin

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
        
    def create(self, validated_data):
      aircraft_data = validated_data.pop('aircraft') # Extract the aircraft data from the validated data
      
      # Check if the aircraft_data passed is the id of an existing aircraft or a new aircraft object
      if is_instance(aircraft_data, int):
        try:
          if Aircraft.objects.get(AircraftID=aircraft_data): # check if an aircraft with the given id exists in the database
            validated_data['aircraft'] = aircraft_data
        except Aircraft.DoesNotExist:
          raise serializer.ValidationError("Aircraft with given ID could not be found in the database")
      elif is_instance(aircraft_data, dict):
        # Create an instance of the Aircraft model
        aircraft = Aircraft.objects.create(
          Model=aircraft_data.get('model'),
          Capacity=aircraft_data.get('capacity')
        )
        
        # Set the value of the key 'aircraft' to the id of the new Aircraft object
        validated_data['aircraft'] = aircraft.AircraftID
      else:
        raise serializer.ValidationError("Flight does not have an associated aircraft")
      
      return Flight.objects.create_flight(**validated_data)
    
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'