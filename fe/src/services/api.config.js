import axios from 'axios';

export const ApiService = axios.create({
    // baseURL: mport.meta.env.VITE_BE_URL, // // // BACKEND URL // // // 
    baseURL: 'http://127.0.0.1:5001/', // // // BACKEND URL // // // 
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
});
