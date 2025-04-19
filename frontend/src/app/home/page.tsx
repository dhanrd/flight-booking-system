"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import axios from 'axios';

// Define types for our data
interface Flight {
  flight_id: number;
  flight_number: string;
  departure_airport: string;
  arrival_airport: string;
  departure_time: string;
  arrival_time: string;
  aircraft_id: number;
}

export default function Home() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [flights, setFlights] = useState<Flight[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Check if user is logged in
    const userData = localStorage.getItem('user');
    
    if (!userData) {
      // Redirect to login if not logged in
      router.push('/login');
      return;
    }
    
    try {
      setUser(JSON.parse(userData));
      fetchFlights();
    } catch (e) {
      // Invalid user data, redirect to login
      localStorage.removeItem('user');
      router.push('/login');
    }
  }, [router]);

  const fetchFlights = async () => {
    setLoading(true);
    try {
      // Fetch flights
      const flightsResponse = await axios.get('http://127.0.0.1:8000/api/flights/');
      const flightData = flightsResponse.data;
      setFlights(flightData);
    } catch (error) {
      console.error('Error fetching flights:', error);
      setError('Failed to load flights. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    router.push('/login');
  };

  const navigateToBookings = () => {
    router.push('/bookings');
  };

  const navigateToMyBookings = () => {
    router.push('/mybookings');
  };

  // Format date for better display
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  // While checking authentication or loading data
  if (!user || loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  // If there was an error loading data
  if (error) {
    return (
      <div className="flex flex-col items-center min-h-screen bg-gray-100 p-8">
        <div className="w-full max-w-4xl bg-white rounded-lg shadow-md p-8">
          <div className="text-red-500">{error}</div>
          <button onClick={fetchFlights} className="mt-4 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-100 p-8">
      <div className="w-full max-w-4xl bg-white rounded-lg shadow-md p-8">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-800">Welcome to Airline Booking System</h1>
          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg"
          >
            Logout
          </button>
        </div>
        
        <div className="mt-4">
          <p className="text-gray-600">
            Welcome, {user.first_name} {user.last_name}!
          </p>
        </div>

        <div className="mt-6 flex gap-6">
          <button
            onClick={navigateToBookings}
            className="bg-green-500 hover:bg-green-600 text-white font-semibold py-3 px-6 rounded-lg"
          >
            Book a Flight
          </button>
        <button
            onClick={navigateToMyBookings}
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg"
          >
            My Bookings
          </button>
        </div>

        {/* Flights Section */}
        <div className="mt-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Available Flights</h2>
          {flights.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full bg-white border border-black">
                <thead>
                  <tr>
                    <th className="text-black py-2 px-4 border-b text-left">Flight #</th>
                    <th className="text-black py-2 px-4 border-b text-left">From</th>
                    <th className="text-black py-2 px-4 border-b text-left">To</th>
                    <th className="text-black py-2 px-4 border-b text-left">Departure</th>
                    <th className="text-black py-2 px-4 border-b text-left">Arrival</th>
                  </tr>
                </thead>
                <tbody>
                  {flights.map((flight) => (
                    <tr key={flight.flight_id} className="hover:bg-gray-50">
                      <td className="text-black py-2 px-4 border-b">{flight.flight_number}</td>
                      <td className="text-black py-2 px-4 border-b">{flight.departure_airport}</td>
                      <td className="text-black py-2 px-4 border-b">{flight.arrival_airport}</td>
                      <td className="text-black py-2 px-4 border-b">{formatDate(flight.departure_time)}</td>
                      <td className="text-black py-2 px-4 border-b">{formatDate(flight.arrival_time)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-gray-500">No flights available.</p>
          )}
        </div>
      </div>
    </div>
  );
}