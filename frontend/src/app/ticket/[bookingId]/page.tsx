"use client";

import { useParams, useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import axios from 'axios';

interface TicketDetails {
  TicketID: number;
  SequenceNumber: number;
  BoardingGroup: string;
  CheckInStatus: string;
  BookingID: number;
}

interface Booking {
  booking_id: number;
  booking_date: string;
  booking_status: string;
  passenger_id: number;
  flight_id: number;
  admin_id: number | null;
}

interface TicketResponse {
  "ticket details": TicketDetails;
}

export default function TicketPage() {
  const router = useRouter();
  const params = useParams();
  const bookingId = params.bookingId as string;
  const [ticketData, setTicketData] = useState<TicketDetails | null>(null);
  const [passengerId, setPassengerId] = useState<number | null>(null);
  const [flightId, setFlightId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const navigateToHome = () => router.push('/home');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // First fetch the ticket data to get the BookingID
        const ticketResponse = await axios.post<TicketResponse>(
          'http://127.0.0.1:8000/api/flight_ticket/',
          { booking_id: bookingId }
        );
        setTicketData(ticketResponse.data["ticket details"]);

        // Then fetch the booking data to get passenger and flight IDs
        const bookingsResponse = await axios.get<Booking[]>(
          'http://127.0.0.1:8000/api/bookings/'
        );

        // Find the booking that matches our ticket's BookingID
        const booking = bookingsResponse.data.find(
          b => b.booking_id === ticketResponse.data["ticket details"].BookingID
        );

        if (!booking) {
          throw new Error('Matching booking not found');
        }

        setPassengerId(booking.passenger_id);
        setFlightId(booking.flight_id);

      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load ticket information');
        console.error('Error fetching data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [bookingId, success]);

  const handleCheckIn = async () => {
    if (!ticketData || passengerId === null || flightId === null) return;

    console.log('Sending check-in data:', {
        ticket_id: ticketData.TicketID,
        passenger_id: passengerId,
        flight_id: flightId,
        check_in_status: "Checked In"
      });

    try {
      setError(null);
      const response = await axios.post(
        'http://127.0.0.1:8000/api/check_in/',
        {
          ticket_id: ticketData.TicketID,
          passenger_id: passengerId,
          flight_id: flightId,
          check_in_status: "Checked In"
        }
      );

      setSuccess(response.data.message || 'Check-in successful!');
      // Refresh the page to update the status
      router.refresh();
    } catch (err: any) {
      setError(
        err.response?.data?.error || 
        err.response?.data?.details || 
        'Failed to complete check-in'
      );
      console.error('Error during check-in:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">Loading...</div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 p-8">
        <div className="max-w-6xl mx-auto">
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6">
            {error}
          </div>
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Ticket #{ticketData?.TicketID}</h1>
          <button 
            onClick={navigateToHome}
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg"
          >
            Home
          </button>
        </div>

        {success && (
          <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-6">
            {success}
          </div>
        )}

        {ticketData && (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h2 className="text-xl font-semibold text-gray-800">Booking #{ticketData.BookingID}</h2>
                  <p className="text-sm text-gray-500">Sequence Number: {ticketData.SequenceNumber}</p>
                </div>
                <div className="flex flex-col items-end">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    ticketData.CheckInStatus === 'Checked In' ? 'bg-green-100 text-green-800' : 
                    ticketData.CheckInStatus === 'Not Checked In' ? 'bg-yellow-100 text-yellow-800' : 
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {ticketData.CheckInStatus}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                <div className="border rounded-lg p-4">
                  <h3 className="text-sm font-medium text-gray-500">Boarding Group</h3>
                  <p className="text-xl font-semibold text-gray-800">{ticketData.BoardingGroup}</p>
                </div>
                
                <div className="border rounded-lg p-4">
                  <h3 className="text-sm font-medium text-gray-500">Check-In Status</h3>
                  <p className="text-xl font-semibold text-gray-800">{ticketData.CheckInStatus}</p>
                </div>
                
                <div className="border rounded-lg p-4">
                  <h3 className="text-sm font-medium text-gray-500">Sequence Number</h3>
                  <p className="text-xl font-semibold text-gray-800">{ticketData.SequenceNumber}</p>
                </div>
              </div>

              <div className="mt-6">
                {ticketData.CheckInStatus === 'Not Checked In' && (
                  <button 
                    onClick={handleCheckIn}
                    className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg"
                  >
                    Check In
                  </button>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}