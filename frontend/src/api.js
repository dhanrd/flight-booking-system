import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const fetchFlights = () => {
    return axios.get(`${API_URL}/flights/`);
};

export const fetchBookings = (userId) => {
    return axios.get(`${API_URL}/bookings/?passenger=${userId}`);
};

export const createBooking = (bookingData) => {
    return axios.post(`${API_URL}/bookings/`, bookingData);
};