import Link from 'next/link';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-md">
        <h1 className="text-3xl font-bold text-center text-gray-800">Airline Booking System</h1>
        <p className="text-center text-gray-600">Welcome to our flight booking platform</p>
        
        <div className="flex flex-col space-y-4 mt-8">
          <Link href="/login" 
            className="w-full py-2 px-4 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg text-center">
            Login
          </Link>
          <Link href="/register"
            className="w-full py-2 px-4 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg text-center">
            Register
          </Link>
        </div>
      </div>
    </div>
  );
}