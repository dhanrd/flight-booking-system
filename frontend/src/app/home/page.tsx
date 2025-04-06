"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function Home() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);

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
    } catch (e) {
      // Invalid user data, redirect to login
      localStorage.removeItem('user');
      router.push('/login');
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('user');
    router.push('/login');
  };

  // While checking authentication
  if (!user) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
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
        
        <div className="mt-8">
          <p className="text-gray-600">You have successfully logged in.</p>
          <p className="text-gray-600 mt-2">
            Welcome, {user.first_name} {user.last_name}!
          </p>
        </div>
      </div>
    </div>
  );
}