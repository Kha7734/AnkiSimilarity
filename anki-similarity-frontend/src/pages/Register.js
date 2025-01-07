import React, { useState } from 'react';
import { registerUser } from '../services/api'; // Import the register function
import { useNavigate } from 'react-router-dom'; // For navigation after registration
import { TextField, Button, Typography, Box, Container, Paper } from '@mui/material'; // Import Material-UI components

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault(); // Prevent form submission
    try {
      const response = await registerUser(username, email, password);
      console.log('Registration successful:', response);
      navigate('/login'); // Redirect to log in after successful registration
    } catch (error) {
      setError('Registration failed. Please try again.');
      console.error('Registration error:', error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ padding: 4, marginTop: 8 }}>
        <Box
          component="form"
          onSubmit={handleRegister}
          sx={{
            display: 'flex',
            flexDirection: 'column',
            gap: 3,
          }}
        >
          <Typography variant="h4" align="center" gutterBottom>
            Register
          </Typography>
          {error && (
            <Typography color="error" align="center">
              {error}
            </Typography>
          )}
          <TextField
            label="Username"
            variant="outlined"
            fullWidth
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <TextField
            label="Email"
            type="email"
            variant="outlined"
            fullWidth
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <TextField
            label="Password"
            type="password"
            variant="outlined"
            fullWidth
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            size="large"
          >
            Register
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default Register;