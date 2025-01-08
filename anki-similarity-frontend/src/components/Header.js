import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { useAuth } from '../AuthContext'; // Import useAuth
import { useNavigate } from 'react-router-dom'; // Import useNavigate for redirection

const Header = () => {
  const { user, logout } = useAuth(); // Get user and logout function from AuthContext
  const navigate = useNavigate(); // Hook for navigation

  const handleLogout = () => {
    logout(); // Call the logout function
    navigate('/login'); // Redirect to the login page
  };

  return (
    <AppBar position="fixed">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          My App
        </Typography>
        {user && ( // Show logout button only if the user is logged in
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Header;