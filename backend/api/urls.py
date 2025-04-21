from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'flights', views.FlightViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'tickets', views.TicketViewSet)
router.register(r'seats', views.SeatViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('search/flights/', views.SearchFlightsView.as_view(), name='search flights'),
    path('search/seats/', views.SearchSeatsView.as_view(), name='search seats'),
    path('booking_summary/', views.CreateBookingView.as_view(), name='booking summary'),
    path('booked_seats/', views.GetBookedSeatsView.as_view(), name='booked seats'),
    path('checkout/', views.PaymentView.as_view(), name='checkout'),
    path('flight_ticket/', views.GetTicketView.as_view(), name='flight ticket'),
    path('check_in/', views.CheckInView.as_view(), name='check in')
]