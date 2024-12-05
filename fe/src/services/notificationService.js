// src/services/notificationPreferences.js
const BASE_URL = "http://127.0.0.1:5001/notificationPreferences";

/**
 * Guarda las preferencias de notificaciones.
 * @param {Object} payload - Datos para guardar las preferencias.
 * @returns {Promise<Response>} Respuesta de la API.
 */
export const saveNotificationPreferences = async (payload) => {
  try {
    const response = await fetch(BASE_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }

    return response.json();
  } catch (error) {
    console.error("Error saving notification preferences:", error);
    throw error;
  }
};
