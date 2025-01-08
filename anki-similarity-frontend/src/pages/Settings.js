import React, { useEffect, useState } from "react";
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  TextField,
  Button,
  Switch,
  FormControlLabel,
} from "@mui/material";
import { useAuth } from "../AuthContext";
import { fetchUserSettings, updateUserSettings } from "../services/api"; // Import settings API functions

const Settings = () => {
  const { user } = useAuth(); // Get the authenticated user from context
  const [settings, setSettings] = useState({
    language_preference: "en",
    daily_goal: 20,
    notification_enabled: true,
    notification_time: "09:00",
    theme: "light",
  });

  // Fetch user settings
  useEffect(() => {
    if (user) {
      const loadUserSettings = async () => {
        try {
          const data = await fetchUserSettings(user.user_id); // Use external function
          setSettings(data);
        } catch (error) {
          console.error("Error loading user settings:", error);
        }
      };

      loadUserSettings();
    }
  }, [user]);

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value, checked, type } = e.target;
    setSettings({
      ...settings,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  // Save settings
  const handleSaveSettings = async () => {
      if (!user) {
        alert("You must be logged in to save settings.");
        return;
      }

      try {
        await updateUserSettings(
          user.user_id,
          settings.language_preference,
          settings.daily_goal,
          settings.notification_enabled,
          settings.notification_time,
          settings.theme
        );
        alert("Settings saved successfully!");
      } catch (error) {
        console.error("Error saving settings:", error);
        alert("Failed to save settings. Please try again.");
      }
    };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      <Card>
        <CardContent>
          <Grid container spacing={3}>
            {/* Language Preference */}
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Language Preference"
                name="language_preference"
                value={settings.language_preference}
                onChange={handleInputChange}
                select
                SelectProps={{ native: true }}
              >
                <option value="en">English</option>
                <option value="vi">Vietnamese</option>
                {/* Add more languages as needed */}
              </TextField>
            </Grid>

            {/* Daily Goal */}
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Daily Goal"
                name="daily_goal"
                type="number"
                value={settings.daily_goal}
                onChange={handleInputChange}
              />
            </Grid>

            {/* Notification Settings */}
            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Switch
                    name="notification_enabled"
                    checked={settings.notification_enabled}
                    onChange={handleInputChange}
                  />
                }
                label="Enable Notifications"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Notification Time"
                name="notification_time"
                type="time"
                value={settings.notification_time}
                onChange={handleInputChange}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>

            {/* Theme */}
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Theme"
                name="theme"
                value={settings.theme}
                onChange={handleInputChange}
                select
                SelectProps={{ native: true }}
              >
                <option value="light">Light</option>
                <option value="dark">Dark</option>
              </TextField>
            </Grid>

            {/* Save Button */}
            <Grid item xs={12}>
              <Button
                variant="contained"
                color="primary"
                onClick={handleSaveSettings}
              >
                Save Settings
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Container>
  );
};

export default Settings;