import axios from 'axios';

const API_URL = '<http://localhost:5000>'; // Replace with your backend URL

export const login = (username, password) => {
  return axios.post(`${API_URL}/login`, { username, password });
};

export const register = (username, email, password) => {
  return axios.post(`${API_URL}/register`, { username, email, password });
};

export const getVocabularyCards = (userId) => {
  return axios.get(`${API_URL}/cards`, { params: { user_id: userId } });
};

