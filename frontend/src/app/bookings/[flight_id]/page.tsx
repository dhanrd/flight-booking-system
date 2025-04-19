"use client";

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import axios from 'axios';

interface Seat {
  SeatID: number;
  SeatNumber: string;
  Class: string;
  Price: number;
}

export default function SeatSelection() {
  const router = useRouter();
  const params = useParams();
  const flight_id = params.flight_id;
  const [user, setUser] = useState<any>(null);
  const [seatClass, setSeatClass] = useState<string>('Economy');
  const [seats, setSeats] = useState<Seat[]>([]);
  const [selectedSeats, setSelectedSeats] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [bookingSuccess, setBookingSuccess] = useState(false);

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (!userData) {
      router.push('/login');
      return;
    }
    setUser(JSON.parse(userData));
  }, [router]);

  useEffect(() => {
    if (user) {
      fetchSeats();
    }
  }, [seatClass, user]);

  const fetchSeats = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/search/seats', {
        flight_id,
        seat_class: seatClass
      });
      
      const availableSeats = response.data['available seats'] || [];
      setSeats(availableSeats.map((seat: any) => ({
        SeatID: seat.SeatID,
        SeatNumber: seat.SeatNumber,
        Class: seat.Class,
        Price: seat.Price,
      })));
      
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to fetch seats');
      setSeats([]);
    } finally {
      setLoading(false);
    }
  };

  const toggleSeatSelection = (seatId: number) => {
    setSelectedSeats(prev => 
      prev.includes(seatId)
        ? prev.filter(id => id !== seatId)
        : [...prev, seatId]
    );
  };

  const handleConfirmBooking = async () => {
    if (selectedSeats.length === 0) return;
    setError('')
    
    try {
      await axios.post('http://127.0.0.1:8000/api/booking_summary', {
        passenger_id: user.UserID,
        flight_id,
        seat_ids: selectedSeats
      });
      setBookingSuccess(true);
      setSelectedSeats([]);
      fetchSeats();
    } catch (err) {
      setError('Failed to confirm booking');
    }
  };

  const goBack = () => {
    router.push('/bookings');
  };

  if (!user) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-100 p-8">
      <div className="w-full max-w-4xl bg-white rounded-lg shadow-md p-8">
        <div className="flex items-center mb-6">
          <button 
            onClick={goBack}
            className="mr-4 bg-gray-200 hover:bg-gray-300 p-2 rounded-full"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M15 18l-6-6 6-6"/>
            </svg>
          </button>
          <h1 className="text-3xl font-bold text-gray-800">Select Your Seats</h1>
        </div>

        <div className="bg-blue-50 p-6 rounded-lg mb-8">
          <h2 className="text-xl font-semibold mb-4 text-blue-800">Seat Selection</h2>
          
          <div className="space-y-4">
            <div>
              <label htmlFor="seatClass" className="block text-sm font-medium text-gray-700 mb-1">
                Seat Class
              </label>
              <select
                id="seatClass"
                value={seatClass}
                onChange={(e) => setSeatClass(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
              >
                <option value="Economy">Economy</option>
                <option value="Business">Business</option>
                <option value="First Class">First Class</option>
              </select>
            </div>
            
            <div className="flex justify-between items-center">
              <div className="text-sm text-gray-600">
                {selectedSeats.length} seat(s) selected
              </div>
              <button
                onClick={fetchSeats}
                disabled={loading}
                className="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                {loading ? 'Loading...' : 'Refresh Seats'}
              </button>
            </div>
          </div>
        </div>

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6">
            <p>{error}</p>
          </div>
        )}

        {seats.length > 0 && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Available {seatClass} Seats</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {seats.map(seat => (
                <div
                  key={seat.SeatID}
                  onClick={() => toggleSeatSelection(seat.SeatID)}
                  className={`p-4 border rounded-lg cursor-pointer ${
                    selectedSeats.includes(seat.SeatID) 
                      ? 'bg-green-100 border-green-500' 
                      : 'bg-white hover:bg-gray-50'
                  }`}
                >
                  <div className="font-medium text-black">Seat: {seat.SeatNumber}</div>
                  <div className="text-black">Class: {seat.Class}</div>
                  <div className="text-black">Price: ${seat.Price}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {selectedSeats.length > 0 && (
          <div className="flex justify-end mt-6">
            <button
              onClick={handleConfirmBooking}
              className="px-6 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
            >
              Confirm Booking ({selectedSeats.length} seats)
            </button>
          </div>
        )}

        {bookingSuccess && (
          <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-6">
            <p>Booking successful! <a href="/mybookings" className="text-blue-600 hover:underline">See my bookings</a></p>
          </div>
        )}

        {seats.length === 0 && !loading && (
          <div className="text-center py-8 text-gray-500">
            {seatClass ? `No seats available in ${seatClass} class. Try another class.` : 'Select a seat class to view available seats'}
          </div>
        )}
      </div>
    </div>
  );
}