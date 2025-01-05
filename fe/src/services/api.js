import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5001"; // Replace with your backend URL
axios.withCredentials = true;

// Items API
export const getItemsByFridgeId = (fridgeId) =>
  axios.get(`${API_BASE_URL}/items/${fridgeId}`);

export const updateItemName = (itemId, userId, newName) =>
  axios.put(`${API_BASE_URL}/items/${itemId}/updateName`, {
    user_id: userId,
    new_name: newName,
  });

export const updateItemExpirationDate = (itemId, userId, newExpirationDate) =>
  axios.put(`${API_BASE_URL}/items/${itemId}/updateExpirationDate`, {
    user_id: userId,
    new_expiration_date: newExpirationDate,
  });

export const addItemsBatch = (items) =>
  axios.post(`${API_BASE_URL}/items/add_batch`, { items });

// Notification Preferences API
export const getNotificationPreferences = (fridgeId) =>
  axios.get(`${API_BASE_URL}/notificationPreferences/${fridgeId}`);
export const saveNotificationPreferences = (preferences) =>
  axios.post(`${API_BASE_URL}/notificationPreferences`, preferences);

//Fetch fridge logs
export const getFridgeLog = (fridgeId) =>
  axios.get(`${API_BASE_URL}/fridges/${fridgeId}/logs`);


// Fridge API
export const linkUserToFridge = async (code) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/link?code=${code}`, {
      withCredentials: true,
    });
    return response; // Devuelve la respuesta para manejarla en el frontend
  } catch (error) {
    console.error("Error in API call to linkUserToFridge:", error);
    throw error; // Lanza el error para manejarlo en el frontend
  }
};

export const checkUserLink = async () => {
  try {
      const response = await axios.get(`${API_BASE_URL}/check_link`, {
          withCredentials: true,
      });
      return response.data.isLinked;
  } catch (error) {
      console.error("Error verifying user link:", error);
      throw error;
  }
};

