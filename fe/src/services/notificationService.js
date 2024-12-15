// // src/services/notificationPreferences.js
// const BASE_URL = "http://192.168.92.67:5001/notificationPreferences";

// /**
//  * Guarda las preferencias de notificaciones.
//  * @param {Object} payload - Datos para guardar las preferencias.
//  * @returns {Promise<Response>} Respuesta de la API.
//  */
// export const saveNotificationPreferences = async (payload) => {
//   try {
//     const response = await fetch(BASE_URL, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify(payload),
//     });

//     if (!response.ok) {
//       throw new Error(`Error: ${response.statusText}`);
//     }

//     return response.json();
//   } catch (error) {
//     console.error("Error saving notification preferences:", error);
//     throw error;
//   }
// };



import { ApiService } from './api.config';

// // // // // NOTIFICATION PREFERENCES // // // // //

export const getAllNotificationPreferences = async () => {
  return ApiService.get('/notificationPreferences/all')
    .then((response) => response.data)
    .catch((response) => Promise.resolve(response));
};

export const getNotificationPreferencesByFridgeId = async (fridgeId) => {
  return ApiService.get(`/notificationPreferences/${fridgeId}`)
    .then((response) => response.data)
    .catch((response) => Promise.resolve(response));
};

export const saveNotificationPreferences = async (request) => {
  return ApiService.post('/notificationPreferences', request)
    .then((response) => response)
    .catch((response) => Promise.resolve(response.response));
};

export const updateNotificationPreferences = async (request) => {
  return ApiService.put('/notificationPreferences', request)
    .then((response) => response)
    .catch((response) => Promise.resolve(response.response));
};
