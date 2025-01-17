import { ApiService } from './api.config'

export const getUserByAuthToken = async () => {
    return ApiService.get(`/user/getUserByAuthToken`, { withCredentials: true })
      .then((response) => response)
      .catch((error) => Promise.resolve(error));
  };
  
export const updateUsername = async (username) => {
    return ApiService.put(`/user/updateUsernameByAuthToken`, { username, withCredentials: true })
      .then((response) => response)
      .catch((error) => Promise.resolve(error));
}
