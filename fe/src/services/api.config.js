import axios from 'axios';

export const ApiService = axios.create({
    // baseURL: mport.meta.env.VITE_BE_URL, // PRODUCTION BACKEND URL
    baseURL: 'http://http://127.0.0.1:5001/', // DEV BACKEND URL
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
});
