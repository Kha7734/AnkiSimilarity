import React, { useState } from 'react';
import { loginUser } from '../services/api'; // Import the login function
import { useNavigate, Link } from 'react-router-dom'; // Thêm Link từ react-router-dom
import { TextField, Button, Typography, Box, Container, Paper } from '@mui/material'; // Import Material-UI components
import { useAuth} from "../AuthContext";

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth(); // Use the login function from AuthContext

  const handleLogin = async (e) => {
    e.preventDefault(); // Prevent form submission
    try {
      const response = await loginUser(username, password);
      login(response.user); // Store the logged-in user in the context
      console.log('Login successful:', response);
      navigate('/dashboard'); // Redirect to dashboard after successful login
    } catch (error) {
      setError('Login failed. Please check your credentials.');
      console.error('Login error:', error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ padding: 4, marginTop: 8 }}>
        <Box
          component="form"
          onSubmit={handleLogin}
          sx={{
            display: 'flex',
            flexDirection: 'column',
            gap: 3,
          }}
        >
          <Typography variant="h4" align="center" gutterBottom>
            Login
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
            Login
          </Button>
          {/* Insert link to register */}
          <Typography align="center" sx={{ marginTop: 2 }}>
            Don't have an account?{' '}
            <Link to="/register" style={{ textDecoration: 'none', color: 'blueviolet' }}>
              Register here
            </Link>
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default Login;