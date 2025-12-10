
import axios from "axios";

const API_URL = "https://spam-detection-backend-vbzq.onrender.com";

export const checkSpam = async (text) => {
  const response = await axios.post(`${API_URL}/check_spam`, {
    text: text,
  });
  return response.data;
};
