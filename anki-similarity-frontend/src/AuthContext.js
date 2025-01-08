import React, { createContext, useState, useContext } from 'react';
import { loginUser } from './services/api'; // Import your login function

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // Add user state

  const login = async (username, password) => {
    try {
      const response = await loginUser(username, password);
      localStorage.setItem('token', response.data.token); // Store the token
      setUser(response.data); // Set the user data
      // console.log('Login successful:', response.data);
      return response;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token'); // Clear the token
    setUser(null); // Clear the user data
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);