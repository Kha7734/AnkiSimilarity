import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000';

const getToken = () => {
  return localStorage.getItem('token'); // Retrieve the token from localStorage
};

// Function to register a user
export const registerUser = async (username, email, password) => {
  try {
    const response = await axios.post(`${API_URL}/register`, {
      username,
      email,
      password,
    }, {
      headers: {
        'Content-Type': 'application/json', // Correct content type
      },
    });
    return response.data;
  } catch (error) {
    console.error('Registration failed:', error.response?.data || error.message);
    throw error;
  }
};

// Function to log in a user
export const loginUser = async (username, password) => {
  try {
    const response = await axios.post(`${API_URL}/login`, {
      username,
      password,
    });
    const { token } = response.data; // Extract the token from the response
    localStorage.setItem('token', token); // Store the token in localStorage
    return response.data;
  } catch (error) {
    console.error('Login failed:', error.response?.data || error.message);
    throw error;
  }
};

// Fetch all datasets for a user
export const fetchDatasets = async (userId) => {
  try {
    const token = getToken(); // Retrieve the token
    const response = await axios.get(`${API_URL}/datasets`, {
      params: { user_id: userId },
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching datasets:", error);
    throw error;
  }
};

// Create a new dataset
export const createDataset = async (userId, name, description) => {
  try {
    const token = getToken(); // Retrieve the token
    const response = await axios.post(`${API_URL}/datasets`, {
      user_id: userId,
      name,
      description,
    }, {
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error creating dataset:", error);
    throw error;
  }
};

// Update an existing dataset
export const updateDataset = async (datasetId, name, description) => {
  try {
    const token = getToken(); // Retrieve the token
    const response = await axios.put(`${API_URL}/datasets/${datasetId}`, {
      name,
      description,
    }, {
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error updating dataset:", error);
    throw error;
  }
};

// Delete a dataset
export const deleteDataset = async (datasetId) => {
  try {
    const token = getToken(); // Retrieve the token
    await axios.delete(`${API_URL}/datasets/${datasetId}`, {
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });
  } catch (error) {
    console.error("Error deleting dataset:", error);
    throw error;
  }
};

// Fetch vocabulary cards for a dataset
export const fetchVocabularyCards = async (datasetId) => {
  try {
    const token = getToken(); // Retrieve the token
    const response = await axios.get(`${API_URL}/datasets/${datasetId}/cards`, {
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching vocabulary cards:", error);
    throw error;
  }
};

// Create a new vocabulary card
export const createVocabularyCard = async (
  userId,
  datasetId,
  word,
  meaning_en,
  meaning_vi,
  ipa_transcription = "",
  example_sentences_en = [],
  example_sentences_vi = [],
  visual_image_url = "",
  audio_url_word = "",
  audio_url_example1 = "",
  audio_url_example2 = "",
  word_type = "",
  vocab_family = [],
  synonyms = [],
  antonyms = []
) => {
  try {
    const token = getToken(); // Retrieve the token
    const response = await axios.post(`${API_URL}/cards`, {
      user_id: userId,
      dataset_id: datasetId,
      word,
      meaning_en,
      meaning_vi,
      ipa_transcription,
      example_sentences_en,
      example_sentences_vi,
      visual_image_url,
      audio_url_word,
      audio_url_example1,
      audio_url_example2,
      word_type,
      vocab_family,
      synonyms,
      antonyms,
    }, {
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error creating vocabulary card:", error);
    throw error;
  }
};

// Update an existing vocabulary card
export const updateVocabularyCard = async (
  cardId,
  word,
  meaning_en,
  meaning_vi,
  ipa_transcription = "",
  example_sentences_en = [],
  example_sentences_vi = [],
  visual_image_url = "",
  audio_url_en = "",
  audio_url_vi = ""
) => {
  try {
    const token = getToken(); // Retrieve the token
    const response = await axios.put(`${API_URL}/cards/${cardId}`, {
      word,
      meaning_en,
      meaning_vi,
      ipa_transcription,
      example_sentences_en,
      example_sentences_vi,
      visual_image_url,
      audio_url_en,
      audio_url_vi,
    }, {
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error updating vocabulary card:", error);
    throw error;
  }
};

// Delete a vocabulary card
export const deleteVocabularyCard = async (cardId) => {
  try {
    const token = getToken(); // Retrieve the token
    await axios.delete(`${API_URL}/cards/${cardId}`, {
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });
  } catch (error) {
    console.error("Error deleting vocabulary card:", error);
    throw error;
  }
};

// Fetch progress for a user
export const fetchUserProgress = async (userId) => {
  try {
    const token = getToken(); // Retrieve the token
    const response = await axios.get(`${API_URL}/api/progress`, {
      params: { user_id: userId },
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching user progress:", error);
    throw error;
  }
};

// Create a new progress entry
export const createProgress = async (userId, cardId, datasetId, status = "new") => {
  try {
    const token = getToken(); // Retrieve the token
    const response = await axios.post(`${API_URL}/api/progress`, {
      user_id: userId,
      card_id: cardId,
      dataset_id: datasetId,
      status,
    }, {
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error creating progress:", error);
    throw error;
  }
};

// Update a progress entry
export const updateProgress = async (
  progressId,
  status,
  lastReviewed,
  nextReview,
  streak,
  easeFactor,
  interval
) => {
  try {
    const token = getToken(); // Retrieve the token
    const response = await axios.put(`${API_URL}/api/progress/${progressId}`, {
      status,
      last_reviewed: lastReviewed,
      next_review: nextReview,
      streak,
      ease_factor: easeFactor,
      interval,
    }, {
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error updating progress:", error);
    throw error;
  }
};

// Delete a progress entry
export const deleteProgress = async (progressId) => {
  try {
    const token = getToken(); // Retrieve the token
    await axios.delete(`${API_URL}/api/progress/${progressId}`, {
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });
  } catch (error) {
    console.error("Error deleting progress:", error);
    throw error;
  }
};

// Fetch settings for a user
export const fetchUserSettings = async (userId) => {
  try {
    const token = getToken(); // Retrieve the token
    const response = await axios.get(`${API_URL}/settings/${userId}`, {
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching user settings:", error);
    throw error;
  }
};

// Create or update user settings
export const updateUserSettings = async (
  userId,
  language_preference,
  daily_goal,
  notification_enabled,
  notification_time,
  theme
) => {
  try {
    const token = getToken(); // Retrieve the token
    const response = await axios.put(`${API_URL}/settings/${userId}`, {
      language_preference,
      daily_goal,
      notification_enabled,
      notification_time,
      theme,
    }, {
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error updating user settings:", error);
    throw error;
  }
};