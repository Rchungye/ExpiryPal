import axios from 'axios';

export const ApiService = axios.create({
    baseURL: 'http://localhost:8080/', // // // BACKEND URL // // // 
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
});
