import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import Register from './Register'; // Adjust the import path
import { registerUser } from '../services/api'; // Mock the API function

// Mock the API function
jest.mock('../services/api', () => ({
  registerUser: jest.fn(),
}));

describe('Register Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  test('renders the registration form', () => {
    render(
      <Router>
        <Register />
      </Router>
    );

    // Check if the form elements are rendered
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /register/i })).toBeInTheDocument();
  });

  test('updates username, email, and password fields', () => {
    render(
      <Router>
        <Register />
      </Router>
    );

    const usernameInput = screen.getByLabelText(/username/i);
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);

    // Simulate user input
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'testpassword' } });

    // Check if the state is updated
    expect(usernameInput.value).toBe('testuser');
    expect(emailInput.value).toBe('test@example.com');
    expect(passwordInput.value).toBe('testpassword');
  });

  test('submits the form with valid credentials', async () => {
    // Mock a successful API response
    registerUser.mockResolvedValueOnce({ data: { message: 'Registration successful' } });

    render(
      <Router>
        <Register />
      </Router>
    );

    const usernameInput = screen.getByLabelText(/username/i);
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const registerButton = screen.getByRole('button', { name: /register/i });

    // Simulate user input and form submission
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'testpassword' } });
    fireEvent.click(registerButton);

    // Wait for the API call to resolve
    await waitFor(() => {
      expect(registerUser).toHaveBeenCalledWith('testuser', 'test@example.com', 'testpassword');
    });
  });

  test('displays an error message on registration failure', async () => {
    // Mock console.error to suppress logs
    jest.spyOn(console, 'error').mockImplementation(() => {});

    // Mock a failed API response
    registerUser.mockRejectedValueOnce(new Error('Registration failed'));

    render(
      <Router>
        <Register />
      </Router>
    );

    const usernameInput = screen.getByLabelText(/username/i);
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const registerButton = screen.getByRole('button', { name: /register/i });

    // Simulate user input and form submission
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'testpassword' } });
    fireEvent.click(registerButton);

    // Wait for the error message to be displayed
    await waitFor(() => {
      expect(screen.getByText(/registration failed/i)).toBeInTheDocument();
    });

    // Restore console.error
    console.error.mockRestore();
  });
});