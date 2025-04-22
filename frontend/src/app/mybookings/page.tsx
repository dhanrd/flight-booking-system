"use client";

import { useState, useEffect } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

interface Booking {
  booking_id: number;
  booking_date: string;
  booking_status: string;
  passenger_id: number;
  flight_id: number;
  admin_id: number | null;
}

interface Flight {
  flight_id: number;
  flight_number: string;
  departure_airport: string;
  arrival_airport: string;
  departure_time: string;
  arrival_time: string;
  aircraft_id: number;
}

interface Seat {
  SeatID: number;
  SeatNumber: string;
  Class: string;
  Price: string;
  FlightID: number;
}

interface BookedSeat {
  booking_id: number;
  seat_id: number;
}

interface BookingWithSeats extends Booking {
  seats: Seat[];
  totalPrice: number;
}

export default function MyBookings() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [bookings, setBookings] = useState<BookingWithSeats[]>([]);
  const [flights, setFlights] = useState<Flight[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const navigateToBookings = () => router.push('/bookings');
  const navigateToHome = () => router.push('/home');

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (!userData) window.location.href = '/login';
    else setUser(JSON.parse(userData));
  }, []);

  useEffect(() => {
    if (!user) return;

    const fetchData = async () => {
      try {
        setLoading(true);
        const [bookingsRes, flightsRes, seatsRes] = await Promise.all([
          axios.get('http://127.0.0.1:8000/api/bookings/'),
          axios.get('http://127.0.0.1:8000/api/flights/'),
          axios.get('http://127.0.0.1:8000/api/seats/')
        ]);

        const userBookings = bookingsRes.data.filter(
          (booking: Booking) => booking.passenger_id === user.UserID
        );

        const bookingsWithSeats = await Promise.all(
          userBookings.map(async (booking: Booking) => {
            const bookedSeatsRes = await axios.post('http://127.0.0.1:8000/api/booked_seats/', {
              booking_id: booking.booking_id
            });

            const bookedSeats = bookedSeatsRes.data.booked_seats as BookedSeat[];
            const seats = seatsRes.data.filter((seat: Seat) => 
              bookedSeats.some(bs => bs.seat_id === seat.SeatID)
            );

            const totalPrice = seats.reduce((sum: number, seat: Seat) => sum + parseFloat(seat.Price), 0);

            return {
              ...booking,
              seats,
              totalPrice
            };
          })
        );

        setFlights(flightsRes.data);
        setBookings(bookingsWithSeats);
      } catch (err) {
        setError('Failed to fetch bookings');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user]);

  if (!user || loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;

  const formatDate = (dateString: string) => new Date(dateString).toLocaleString();

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">My Bookings</h1>
          <div className="flex gap-4">
            <button onClick={navigateToHome} className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg">
              Home
            </button>
            <button onClick={navigateToBookings} className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg">
              Book a Flight
            </button>
          </div>
        </div>

        {error && <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6">{error}</div>}

        {bookings.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <p className="text-gray-600">You don't have any bookings yet.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {bookings.map(booking => {
              const flight = flights.find(f => f.flight_id === booking.flight_id);
              return (
                <div key={booking.booking_id} className="bg-white rounded-lg shadow overflow-hidden">
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h2 className="text-xl font-semibold text-gray-800">Booking #{booking.booking_id}</h2>
                        <p className="text-sm text-gray-500">Booked on: {formatDate(booking.booking_date)}</p>
                      </div>
                      <div className="flex flex-col items-end">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                          booking.booking_status === 'Confirmed' ? 'bg-green-100 text-green-800' : 
                          booking.booking_status === 'Pending' ? 'bg-yellow-100 text-yellow-800' : 
                          'bg-red-100 text-red-800'
                        }`}>
                          {booking.booking_status}
                        </span>
                        <p className="mt-2 text-lg font-semibold text-gray-500">Total Price: ${booking.totalPrice.toFixed(2)}</p>
                      </div>
                    </div>

                    {flight && (
                      <>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                          <div>
                            <h3 className="text-sm font-medium text-gray-500">Flight Number</h3>
                            <p className="text-lg font-semibold text-gray-500">{flight.flight_number}</p>
                          </div>
                          <div>
                            <h3 className="text-sm font-medium text-gray-500">Departure</h3>
                            <p className="text-lg font-semibold text-gray-500">{flight.departure_airport}</p>
                            <p className="text-sm text-gray-500">{formatDate(flight.departure_time)}</p>
                          </div>
                          <div>
                            <h3 className="text-sm font-medium text-gray-500">Arrival</h3>
                            <p className="text-lg font-semibold text-gray-500">{flight.arrival_airport}</p>
                            <p className="text-sm text-gray-500">{formatDate(flight.arrival_time)}</p>
                          </div>
                        </div>

                        {booking.seats.length > 0 && (
                          <div className="mt-6">
                            <h3 className="text-lg font-semibold text-gray-800 mb-3">Booked Seats</h3>
                            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 text-gray-500">
                              {booking.seats.map(seat => (
                                <div key={seat.SeatID} className="border rounded-lg p-4">
                                  <p className="font-semibold">Seat: {seat.SeatNumber}</p>
                                  <p>Class: {seat.Class}</p>
                                  <p>Price: ${seat.Price}</p>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
  
                        <div className="mt-6 flex gap-4">
                          {booking.booking_status === 'Pending' && (
                            <button 
                              className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg"
                              onClick={() => router.push(`/checkout/${booking.booking_id}?totalPrice=${booking.totalPrice}`)}
                            >
                              Pay Booking
                            </button>
                          )}
                          {booking.booking_status === 'Confirmed' && (
                            <button 
                              className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg"
                              onClick={() => router.push(`/ticket/${booking.booking_id}`)}
                            >
                              View Ticket
                            </button>
                          )}
                        </div>
                      </>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}