import axios from 'axios';

export const ApiService = axios.create({
    // baseURL: mport.meta.env.VITE_BE_URL, // PRODUCTION BACKEND URL
    baseURL: 'http://localhost:8080/', // DEV BACKEND URL
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
});
