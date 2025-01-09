/* eslint-env serviceworker */
/* eslint-disable no-undef */
importScripts('https://www.gstatic.com/firebasejs/10.13.2/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.13.2/firebase-messaging-compat.js');

// Initialize the Firebase app in the service worker by passing in
// your app's Firebase config object.
// https://firebase.google.com/docs/web/setup#config-object
firebase.initializeApp({
    apiKey: "AIzaSyDMyQXDBjaslet1niB2Ykbw8lNJuu6pSdg",
    authDomain: "expirypalnotifications.firebaseapp.com",
    projectId: "expirypalnotifications",
    storageBucket: "expirypalnotifications.firebasestorage.app",
    messagingSenderId: "728246427019",
    appId: "1:728246427019:web:d6b56a279521ace757a38e",
    measurementId: "G-3MP62M8QHK"
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
    console.log(
      '[firebase-messaging-sw.js] Received background message ',
      payload
    );
    // Customize notification here
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
      body: payload.notification.body,
      icon: payload.notification.image,
    };
  
    self.registration.showNotification(notificationTitle, notificationOptions);
  });