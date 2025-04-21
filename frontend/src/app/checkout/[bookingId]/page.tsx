"use client";

import { useRouter, useSearchParams, useParams } from 'next/navigation';
import { useState } from 'react';
import axios from 'axios';

export default function CheckoutPage() {
  const router = useRouter();
  const params = useParams();
  const searchParams = useSearchParams();
  
  const bookingId = params.bookingId as string;
  const totalPrice = searchParams.get('totalPrice') || '0.00';
  const [paymentStatus, setPaymentStatus] = useState<'idle' | 'processing' | 'success' | 'error'>('idle');

  const goBack = () => router.push('/mybookings');

  const handlePayment = async () => {
    setPaymentStatus('processing');
    
    try {
      await axios.post('http://127.0.0.1:8000/api/checkout/', {
        booking_id: bookingId,
        payment_amount: totalPrice
      });
      
      setPaymentStatus('success');
    } catch (error) {
      setPaymentStatus('error');
      console.error('Payment failed:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center mb-6">
          <button 
            onClick={goBack}
            className="mr-4 bg-gray-200 hover:bg-gray-300 p-2 rounded-full"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M15 18l-6-6 6-6"/>
            </svg>
          </button>
          <h1 className="text-2xl font-bold text-gray-800">Complete Your Payment</h1>
        </div>

        <div className="space-y-6">
          <div className="space-y-2">
            <p className="text-sm font-medium text-gray-500">Booking Reference</p>
            <p className="text-lg font-semibold text-gray-500">{bookingId}</p>
          </div>
          
          <div className="space-y-2">
            <p className="text-sm font-medium text-gray-500">Amount Due</p>
            <p className="text-2xl font-bold text-green-600">${totalPrice}</p>
          </div>

          <div className="space-y-4 border-t pt-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Name on Card</label>
              <input 
                type="text" 
                placeholder="John Doe" 
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Card Number</label>
              <input 
                type="text" 
                placeholder="4242 4242 4242 4242" 
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-500"
              />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Expiry</label>
                <input 
                  type="text" 
                  placeholder="MM/YY" 
                  className="w-full px-4 py-2 border rounded-lg text-gray-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">CVC</label>
                <input 
                  type="text" 
                  placeholder="123" 
                  className="w-full px-4 py-2 border rounded-lg text-gray-500"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Zip/Postal Code</label>
              <input 
                type="text" 
                placeholder="10001" 
                className="w-full px-4 py-2 border rounded-lg text-gray-500"
              />
            </div>
          </div>

          {/* Payment Status Feedback */}
          {paymentStatus === 'success' && (
            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
              Payment confirmed!
            </div>
          )}
          
          {paymentStatus === 'error' && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              Payment failed. Please try again.
            </div>
          )}

          <button 
            onClick={handlePayment}
            disabled={paymentStatus === 'processing'}
            className={`w-full py-3 px-4 rounded-lg font-semibold ${
              paymentStatus === 'processing' 
                ? 'bg-blue-300 cursor-not-allowed' 
                : 'bg-blue-500 hover:bg-blue-600 text-white'
            }`}
          >
            {paymentStatus === 'processing' ? 'Processing...' : 'Confirm Payment'}
          </button>
        </div>
      </div>
    </div>
  );
}