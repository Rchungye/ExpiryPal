// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";

import { getMessaging, getToken } from "firebase/messaging";

const firebaseConfig = {
  apiKey: "AIzaSyDMyQXDBjaslet1niB2Ykbw8lNJuu6pSdg",
  authDomain: "expirypalnotifications.firebaseapp.com",
  projectId: "expirypalnotifications",
  storageBucket: "expirypalnotifications.firebasestorage.app",
  messagingSenderId: "728246427019",
  appId: "1:728246427019:web:d6b56a279521ace757a38e",
  measurementId: "G-3MP62M8QHK"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const messaging = getMessaging(app);

export const generateToken= async () => {
    const permission = await Notification.requestPermission();
    if (permission === "granted") {
        const token = await getToken(messaging, {
            vapidKey: "BJtvOoDCBR56TPia4X56ugxgUlQkz0nKslsmx-IWxqdH4dt43y3R9zkKLAwQVwqXoRmm3zjlPt0yUrXs825TjN0"
        })
        sendTokenToServer(token);
    }
}
export const sendTokenToServer = async (token) => {
    try {
        const response = await fetch('/api/register-token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token }),
            credentials: 'include', // Incluye las cookies en la solicitud
        });

        if (response.ok) {
            console.log('Token sent to server successfully.');
        } else {
            console.error('Failed to send token to server. Response status:', response.status);
        }
    } catch (error) {
        console.error('Error sending token to server:', error);
    }
};
