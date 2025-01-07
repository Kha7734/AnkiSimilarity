import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import Login from './Login'; // Adjust the import path
import { loginUser } from '../services/api'; // Mock the API function

// Mock the API function
jest.mock('../services/api', () => ({
  loginUser: jest.fn(),
}));

describe('Login Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  test('renders the login form', () => {
    render(
      <Router>
        <Login />
      </Router>
    );

    // Check if the form elements are rendered
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  test('updates username and password fields', () => {
    render(
      <Router>
        <Login />
      </Router>
    );

    const usernameInput = screen.getByLabelText(/username/i);
    const passwordInput = screen.getByLabelText(/password/i);

    // Simulate user input
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'testpassword' } });

    // Check if the state is updated
    expect(usernameInput.value).toBe('testuser');
    expect(passwordInput.value).toBe('testpassword');
  });

  test('submits the form with valid credentials', async () => {
    // Mock a successful API response
    loginUser.mockResolvedValueOnce({ data: { message: 'Login successful' } });

    render(
      <Router>
        <Login />
      </Router>
    );

    const usernameInput = screen.getByLabelText(/username/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const loginButton = screen.getByRole('button', { name: /login/i });

    // Simulate user input and form submission
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'testpassword' } });
    fireEvent.click(loginButton);

    // Wait for the API call to resolve
    await waitFor(() => {
      expect(loginUser).toHaveBeenCalledWith('testuser', 'testpassword');
    });
  });

  test('displays an error message on login failure', async () => {
      // Mock console.error to suppress logs
      jest.spyOn(console, 'error').mockImplementation(() => {});

      // Mock a failed API response
      loginUser.mockRejectedValueOnce(new Error('Invalid credentials'));

      render(
        <Router>
          <Login />
        </Router>
      );

      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const loginButton = screen.getByRole('button', { name: /login/i });

      // Simulate user input and form submission
      fireEvent.change(usernameInput, { target: { value: 'testuser' } });
      fireEvent.change(passwordInput, { target: { value: 'testpassword' } });
      fireEvent.click(loginButton);

      // Wait for the error message to be displayed
      await waitFor(() => {
        expect(screen.getByText(/login failed/i)).toBeInTheDocument();
      });

      // Restore console.error
      console.error.mockRestore();
    });

});