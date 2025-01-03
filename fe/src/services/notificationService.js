import { ApiService } from './api.config';

// // // // // NOTIFICATION PREFERENCES // // // // //

export const getAllNotificationPreferences = async () => {
  return ApiService.get('/notificationPreferences/all')
    .then((response) => response.data)
    .catch((response) => Promise.resolve(response));
};

export const getNotificationPreferences = async (fridgeId) => {
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
