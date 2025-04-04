from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import Booking, Flight, Ticket, User, Passenger
from .serializers import BookingSerializer, TicketSerializer, UserSerializer, PassengerSerializer, FlightSerializer

class RegisterView(APIView):
    def post(self, request):
        # Create User
        user_serializer = UserSerializer(data=request.data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = user_serializer.save()

        # Create Passenger
        passenger_data = {
            'PassengerID': user.UserID,
            'Status': 'Active'
        }
        passenger_serializer = PassengerSerializer(data=passenger_data)
        
        if passenger_serializer.is_valid():
            try:
                passenger = passenger_serializer.save()
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