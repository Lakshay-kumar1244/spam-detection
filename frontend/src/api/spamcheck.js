import axios from "axios";

export const checkSpam = async (text) => {
  const response = await axios.post("http://127.0.0.1:8000/check_spam", {
    text: text,
  });

  return response.data;
};