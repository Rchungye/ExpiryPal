import { ApiService } from './api.config';

// // // // // ITEM SERVICE // // // // //

export const getItemsByFridgeId = async (fridgeId) => {
  return ApiService.get(`/items/${fridgeId}`)
    .then((response) => response)
    .catch((response) => Promise.resolve(response));
};

export const updateItemName = async (itemId, userId, newName) => {
  return ApiService.put(`/items/${itemId}/updateName`, {
    user_id: userId,
    new_name: newName,
  })
    .then((response) => response)
    .catch((response) => Promise.resolve(response.response));
};

export const updateItemExpirationDate = async (itemId, userId, newExpirationDate) => {
  return ApiService.put(`/items/${itemId}/updateExpirationDate`, {
    user_id: userId,
    new_expiration_date: newExpirationDate,
  })
    .then((response) => response)
    .catch((response) => Promise.resolve(response.response));
};

export const addItemsBatch = async (items) => {
  return ApiService.post('/items/add_batch', { items })
    .then((response) => response)
    .catch((response) => Promise.resolve(response.response));
};
