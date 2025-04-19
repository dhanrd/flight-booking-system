"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
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

export default function BookingSearch() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [searchResults, setSearchResults] = useState<Flight[]>([]);
  const [error, setError] = useState('');
  const [searchParams, setSearchParams] = useState({
    departure_airport: '',
    arrival_airport: ''
  });

  useEffect(() => {
    // Check if user is logged in
    const userData = localStorage.getItem('user');
    console.log(userData);
    
    if (!userData) {
      // Redirect to login if not logged in
      router.push('/login');
      return;
    }
    
    try {
      setUser(JSON.parse(userData));
    } catch (e) {
      // Invalid user data, redirect to login
      localStorage.removeItem('user');
      router.push('/login');
    }
  }, [router]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setSearchParams(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSearchResults([]);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/search/flights', searchParams);
      
      if (response.data && response.data['available flights']) {
        setSearchResults(response.data['available flights']);
      } else {
        setSearchResults([]);
      }
    } catch (err: any) {
      console.error('Search error:', err);
      if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error);
      } else {
        setError('Failed to search flights. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const goBack = () => {
    router.push('/home');
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
          <h1 className="text-3xl font-bold text-gray-800">Book a Flight</h1>
        </div>

        <div className="bg-blue-50 p-6 rounded-lg mb-8">
          <h2 className="text-xl font-semibold mb-4 text-blue-800">Search Flights</h2>
          
          <form onSubmit={handleSearch} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="departure_airport" className="block text-sm font-medium text-gray-700 mb-1">
                  Departure Airport
                </label>
                <input
                  id="departure_airport"
                  name="departure_airport"
                  type="text"
                  value={searchParams.departure_airport}
                  onChange={handleChange}
                  required
                  placeholder="e.g., YYC"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
                />
              </div>
              
              <div>
                <label htmlFor="arrival_airport" className="block text-sm font-medium text-gray-700 mb-1">
                  Arrival Airport
                </label>
                <input
                  id="arrival_airport"
                  name="arrival_airport"
                  type="text"
                  value={searchParams.arrival_airport}
                  onChange={handleChange}
                  required
                  placeholder="e.g., YVR"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
                />
              </div>
            </div>
            
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                {loading ? 'Searching...' : 'Search Flights'}
              </button>
            </div>
          </form>
        </div>

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6">
            <p>{error}</p>
          </div>
        )}

        {searchResults.length > 0 && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Search Results</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full bg-white border border-gray-300">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-black py-3 px-4 border-b text-left">Flight #</th>
                    <th className="text-black py-3 px-4 border-b text-left">From</th>
                    <th className="text-black py-3 px-4 border-b text-left">To</th>
                    <th className="text-black py-3 px-4 border-b text-left">Departure</th>
                    <th className="text-black py-3 px-4 border-b text-left">Arrival</th>
                    <th className="text-black py-3 px-4 border-b text-left">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {searchResults.map((flight) => (
                    <tr key={flight.flight_id} className="hover:bg-gray-50">
                      <td className="text-black py-3 px-4 border-b">{flight.flight_number}</td>
                      <td className="text-black py-3 px-4 border-b">{flight.departure_airport}</td>
                      <td className="text-black py-3 px-4 border-b">{flight.arrival_airport}</td>
                      <td className="text-black py-3 px-4 border-b">{formatDate(flight.departure_time)}</td>
                      <td className="text-black py-3 px-4 border-b">{formatDate(flight.arrival_time)}</td>
                      <td className="text-black py-3 px-4 border-b">
                        <button 
                          onClick={() => router.push(`/bookings/${flight.flight_id}`)}
                          className="px-4 py-1 bg-green-500 hover:bg-green-600 text-white font-medium rounded"
                        >
                          Select
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
        
        {searchResults.length === 0 && !loading && !error && searchParams.departure_airport && searchParams.arrival_airport && (
          <div className="text-center py-8 text-gray-500">
            No flights found matching your search criteria.
          </div>
        )}
      </div>
    </div>
  );
}