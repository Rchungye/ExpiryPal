// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";

import { getMessaging, getToken } from "firebase/messaging";
import { sendTokenToServer } from "../services/api";

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
    console.log("Requesting permission...");
    console.log("in generateToken");
    const permission = await Notification.requestPermission();
    if (permission === "granted") {
        const token = await getToken(messaging, {
            vapidKey: "BJtvOoDCBR56TPia4X56ugxgUlQkz0nKslsmx-IWxqdH4dt43y3R9zkKLAwQVwqXoRmm3zjlPt0yUrXs825TjN0"
        })
        sendTokenToServer(token);
    }
}