import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000';

// Function to register a user
export const registerUser = async (username, email, password) => {
  try {
    const response = await axios.post(`${API_URL}/register`, {
      username,
      email,
      password,
    });
    return response.data; // Return the response from the backend
  } catch (error) {
    console.error('Registration failed:', error.response?.data || error.message);
    throw error;
  }
};

export const loginUser = async (username, password) => {
  try {
    const response = await axios.post(`${API_URL}/login`, {
      username,
      password,
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data; // Trả về phản hồi từ back-end
  } catch (error) {
    console.error('Login failed:', error.response?.data || error.message);
    throw error;
  }
};

// Fetch all datasets for a user
export const fetchDatasets = async (userId) => {
  try {
    const response = await axios.get(`${API_URL}/datasets`, {
      params: { user_id: userId },
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
    const response = await axios.post(`${API_URL}/datasets`, {
      user_id: userId,
      name,
      description,
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
    const response = await axios.put(`${API_URL}/datasets/${datasetId}`, {
      name,
      description,
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
    await axios.delete(`${API_URL}/datasets/${datasetId}`);
  } catch (error) {
    console.error("Error deleting dataset:", error);
    throw error;
  }
};

// Fetch vocabulary cards for a dataset
export const fetchVocabularyCards = async (datasetId) => {
  try {
    const response = await axios.get(`${API_URL}/datasets/${datasetId}/cards`);
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
  audio_url_en = "",
  audio_url_vi = ""
) => {
  try {
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
      audio_url_en,
      audio_url_vi,
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
    await axios.delete(`${API_URL}/cards/${cardId}`);
  } catch (error) {
    console.error("Error deleting vocabulary card:", error);
    throw error;
  }
};

// Fetch progress for a user
export const fetchUserProgress = async (userId) => {
  try {
    const response = await axios.get(`${API_URL}/api/progress`, {
      params: { user_id: userId },
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
    const response = await axios.post(`${API_URL}/api/progress`, {
      user_id: userId,
      card_id: cardId,
      dataset_id: datasetId,
      status,
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
    const response = await axios.put(`${API_URL}/api/progress/${progressId}`, {
      status,
      last_reviewed: lastReviewed,
      next_review: nextReview,
      streak,
      ease_factor: easeFactor,
      interval,
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
    await axios.delete(`${API_URL}/api/progress/${progressId}`);
  } catch (error) {
    console.error("Error deleting progress:", error);
    throw error;
  }
};