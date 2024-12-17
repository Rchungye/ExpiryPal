import { ApiService } from './api.config'

// // // // // FRIDGE LOG SERVICE // // // // //

export const getFridgeLog = async (fridgeId) => {
    return ApiService.get(`/fridges/${fridgeId}/logs`)
      .then((response) => response)
      .catch((response) => Promise.resolve(response));
  };


