from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import authenticate
from .models import Booking, Flight, Ticket, User, Passenger, Seat
from .serializers import BookingSerializer, TicketSerializer, UserSerializer, PassengerSerializer, FlightSerializer, SeatSerializer

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
        
        # Create BookingSeat record once we've creating Booking record to access BookingID
        booking_seat_data = {
          'booking_id' : flight_booking.BookingID,
          'seat_id' : request.data.get('seat_id')
        }

        bookingseat_serializer = BookingSeatSerializer(data=booking_seat_data)
        if not bookingseat_serializer.is_valid():
          flight_booking.delete()
          return Response({
            'error' : 'Error occured while reserving seat',
            'details' : bookingseat_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
        bookingseat_serializer.save()
        
        return Response({
          'message' : 'Flight booking successfully created',
          'booking details' : booking_serializer.data,
          'booking seat details' : booking_seat_serializer.data,
        }, status=status.HTTP_201_CREATED)
      except Exception as e:
        return Response({
          'error' : 'Error occured while creating flight booking',
          'details' : str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    else:
      return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
  

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer