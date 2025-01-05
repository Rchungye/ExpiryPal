import axios from 'axios';

axios.defaults.withCredentials = true;

export const ApiService = axios.create({
    baseURL: import.meta.env.VITE_BE_URL, // // // BACKEND URL // // // 
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
});
