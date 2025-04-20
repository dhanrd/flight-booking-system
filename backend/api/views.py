from django.conf import settings

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import authenticate
from .models import Booking, Flight, Ticket, User, Passenger, Seat, BookingSeat, Payment
from .serializers import BookingSerializer, TicketSerializer, UserSerializer, PassengerSerializer, FlightSerializer, SeatSerializer, BookingSeatSerializer, PaymentSerializer

import random 

class RegisterView(APIView):
    def post(self, request):
        # Separate user and passenger data
        user_data = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'date_of_birth': request.data.get('date_of_birth'),
            'phone_number': request.data.get('phone_number')
        }
        
        passenger_data = {
            'PassportNumber': request.data.get('passport_number'),
            'LoyaltyNumber': request.data.get('loyalty_number'),
            'Status': request.data.get('status', 'Active')  # Default active
        }

        # Create User
        user_serializer = UserSerializer(data=user_data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = user_serializer.save()

        # Create Passenger with the user's ID
        passenger_data['PassengerID'] = user.UserID
        passenger_serializer = PassengerSerializer(data=passenger_data)
        
        if passenger_serializer.is_valid():
            try:
                passenger_serializer.save()
                return Response({
                    'user': user_serializer.data,
                    'passenger': passenger_serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                user.delete()
                return Response({
                    'error': 'Database error creating passenger',
                    'details': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            user.delete()
            return Response({
                'error': 'Invalid passenger data',
                'details': passenger_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                serializer = UserSerializer(user)
                return Response({'user': serializer.data})
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
 
class SearchFlightsView(APIView):
    def post(self, request):
      departure_airport = request.data.get('departure_airport')
      arrival_airport = request.data.get('arrival_airport')
      
      try:
        flights = Flight.objects.get_flights_by_airports(departure_airport, arrival_airport) 
        serializer = FlightSerializer(flights, many=True) # allow us to serialize many flights
        return Response({ 'available flights' : serializer.data})
      except Flight.DoesNotExist:
        return Response({'error: Flights not found based on provided criteria'}, status=status.HTTP_404_NOT_FOUND)
      
class SearchSeatsView(APIView):
    def post(self, request):
      flight_id = request.data.get('flight_id')
      seat_class = request.data.get('seat_class')
      
      try:
        seats = Seat.objects.get_available_seats(flight_id, seat_class) 
        serializer = SeatSerializer(seats, many=True) # allow us to serialize many seats
        return Response({
          'available seats': serializer.data
        })
      except Seat.DoesNotExist:
        return Response({'error: Seats not available for provided class'}, status=status.HTTP_404_NOT_FOUND)
      
class GetBookedSeatsView(APIView):
  def post(self, request):
    booking_id = request.data.get('booking_id')
    
    try:
      booked_seats = BookingSeat.objects.filter(booking_id=booking_id).values('booking_id', 'seat_id')

      return Response({
        'booking_id' : booking_id,
        'booked_seats' : list(booked_seats)
      }, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({
        'error' : 'Error occured while retrieving booked seats',
        'message' : 'Could not find any booked seats associated with the provided booking id',
        'details' : str(e)
      }, status=status.HTTP_404_NOT_FOUND)
      
class CreateBookingView(APIView):
  def post(self, request):
    booking_data = {
      'passenger_id': request.data.get('passenger_id'),
      'flight_id' : request.data.get('flight_id'),
      'booking_status' :  request.data.get('booking_status', 'Pending'), # default to 'Pending'
      'admin_id' : request.data.get('admin_id')
    }
    
    booking_serializer = BookingSerializer(data=booking_data) # pass booking data to BookingSerializer class
    
    if booking_serializer.is_valid():
      try:
        flight_booking = booking_serializer.save() # save and return Booking record
        
        seats_id = request.data.get('seat_ids', [])
        booked_seats = []
        
        for seat_id in seats_id:
          # Create BookingSeat record once we've creating Booking record to access BookingID
          booking_seat_data = {
            'booking_id' : flight_booking.booking_id,
            'seat_id' : seat_id
          }

          booking_seat_serializer = BookingSeatSerializer(data=booking_seat_data)

          if not booking_seat_serializer.is_valid():
            flight_booking.delete()
            return Response({
              'error' : 'Error occured while reserving seat',
              'details' : booking_seat_serializer.errors
              }, status=status.HTTP_400_BAD_REQUEST)
      
          booked_seat = booking_seat_serializer.save()
          booked_seats.append(BookingSeatSerializer(booked_seat).data)
          
        return Response({
          'message' : 'Flight booking successfully created',
          'booking details' : booking_serializer.data,
          'booking seat details' : booked_seats,
        }, status=status.HTTP_201_CREATED)
      except Exception as e:
        return Response({
          'error' : 'Error occured while creating flight booking',
          'details' : str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    else:
      return Response({
        "error" : "Error while creating booking",
        "details" : booking_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
  
class PaymentView(APIView):
  def post(self, request):
    payment_data = {
      'BookingID' : request.data.get('booking_id'),
      'Amount' : request.data.get('payment_amount')
    } 
    
    payment_serializer = PaymentSerializer(data=payment_data)
    
    if payment_serializer.is_valid():
      try:
        payment_serializer.save() # save payment record
        
        booking = Booking.objects.get(booking_id=payment_serializer.data['BookingID']) # get the booking associated with the current payment
        booking.booking_status = 'Confirmed' # update the booking status to 'Confirmed' once payment is completed
        booking.save() # save updated Booking record 
      
        booking_serializer = BookingSerializer(booking) # serialize 'booking' model instance

        # Generate Ticket record
        ticket_data = {
          'BookingID' : booking.booking_id,
          'SequenceNumber' : random.randint(100000, 999999),
          'BoardingGroup' : 'Group ' + random.choice(['A', 'B', 'C', 'D', 'E']),
          'CheckInStatus' : 'Not Checked In'
        }
        
        ticket_serializer = TicketSerializer(data=ticket_data)
        
        if ticket_serializer.is_valid():
          try:
            ticket_serializer.save() # Save Ticket record to database
          except Exception as e:
            return Response({
              'error' : 'Error occurred while saving ticket to database',
              'details' : str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response({
              "error" : "Error while generating ticket",
              "details" : ticket_serializer.errors
              }, status=status.HTTP_400_BAD_REQUEST)
                    
        return Response({
          'message' : 'Payment made successfully',
          'payment details' : payment_serializer.data,
          'booking details' : booking_serializer.data,
          'ticket details' : ticket_serializer.data
        }, status=status.HTTP_200_OK)
      except Exception as e:
        return Response({
          'error' : 'Error occured while processing payment',
          'details' : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
      return Response({
        'error' : 'Payment validation failed',
        'message' : 'Please check the submitted payment information',
        'details' : payment_serializer.errors
      }, status=status.HTTP_400_BAD_REQUEST)
          
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer