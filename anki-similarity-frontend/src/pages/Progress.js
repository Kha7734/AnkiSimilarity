import React, { useEffect, useState } from "react";
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  List,
  ListItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from "@mui/material";
import { useAuth } from "../AuthContext"; // Import useAuth
import {
  fetchUserProgress,
  createProgress,
  updateProgress,
  deleteProgress,
} from "../services/api"; // Import progress API functions

const Progress = () => {
  const [userProgress, setUserProgress] = useState([]);
  const [newProgress, setNewProgress] = useState({
    card_id: "",
    dataset_id: "",
    status: "new",
  });
  const [editProgress, setEditProgress] = useState(null); // Progress entry being edited
  const [openEditDialog, setOpenEditDialog] = useState(false); // Edit dialog state
  const { user } = useAuth(); // Get the authenticated user from context

  // Fetch user progress
  useEffect(() => {
    if (user) {
      const loadUserProgress = async () => {
        try {
          const data = await fetchUserProgress(user._id); // Use external function
          setUserProgress(data);
        } catch (error) {
          console.error("Error loading user progress:", error);
        }
      };

      loadUserProgress();
    }
  }, [user]);

  // Add a new progress entry
  const handleAddProgress = async () => {
    if (!user) return; // Ensure the user is authenticated
    try {
      const newEntry = await createProgress(
        user._id,
        newProgress.card_id,
        newProgress.dataset_id,
        newProgress.status
      ); // Use external function
      setUserProgress([...userProgress, newEntry]);
      setNewProgress({ card_id: "", dataset_id: "", status: "new" });
    } catch (error) {
      console.error("Error adding progress:", error);
    }
  };

  // Open edit dialog for a progress entry
  const handleEditProgress = (progress) => {
    setEditProgress(progress);
    setOpenEditDialog(true);
  };

  // Update a progress entry
  const handleUpdateProgress = async () => {
    try {
      const updatedEntry = await updateProgress(
        editProgress.progress_id,
        editProgress.status,
        editProgress.last_reviewed,
        editProgress.next_review,
        editProgress.streak,
        editProgress.ease_factor,
        editProgress.interval
      ); // Use external function
      setUserProgress(
        userProgress.map((progress) =>
          progress.progress_id === editProgress.progress_id ? updatedEntry : progress
        )
      );
      setOpenEditDialog(false);
    } catch (error) {
      console.error("Error updating progress:", error);
    }
  };

  // Delete a progress entry
  const handleDeleteProgress = async (progressId) => {
    try {
      await deleteProgress(progressId); // Use external function
      setUserProgress(userProgress.filter((progress) => progress.progress_id !== progressId));
    } catch (error) {
      console.error("Error deleting progress:", error);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        User Progress
      </Typography>

      {/* Add New Progress Form */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Card ID"
            value={newProgress.card_id}
            onChange={(e) => setNewProgress({ ...newProgress, card_id: e.target.value })}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Dataset ID"
            value={newProgress.dataset_id}
            onChange={(e) => setNewProgress({ ...newProgress, dataset_id: e.target.value })}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Status"
            value={newProgress.status}
            onChange={(e) => setNewProgress({ ...newProgress, status: e.target.value })}
          />
        </Grid>
        <Grid item xs={12}>
          <Button variant="contained" color="primary" onClick={handleAddProgress}>
            Add Progress
          </Button>
        </Grid>
      </Grid>

      {/* User Progress List */}
      <Grid container spacing={3}>
        {userProgress.map((progress) => (
          <Grid item xs={12} md={6} key={progress.progress_id}>
            <Card>
              <CardContent>
                <Typography variant="h6">Card ID: {progress.card_id}</Typography>
                <Typography variant="body1">Dataset ID: {progress.dataset_id}</Typography>
                <Typography variant="body1">Status: {progress.status}</Typography>
                <Typography variant="body2" color="textSecondary">
                  Last Reviewed: {progress.last_reviewed || "Never"}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Next Review: {progress.next_review || "Not scheduled"}
                </Typography>
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={() => handleEditProgress(progress)}
                >
                  Edit
                </Button>
                <Button
                  variant="outlined"
                  color="secondary"
                  onClick={() => handleDeleteProgress(progress.progress_id)}
                >
                  Delete
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Edit Progress Dialog */}
      <Dialog open={openEditDialog} onClose={() => setOpenEditDialog(false)}>
        <DialogTitle>Edit Progress</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Status"
            value={editProgress?.status || ""}
            onChange={(e) => setEditProgress({ ...editProgress, status: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Last Reviewed"
            type="datetime-local"
            value={editProgress?.last_reviewed || ""}
            onChange={(e) =>
              setEditProgress({ ...editProgress, last_reviewed: e.target.value })
            }
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Next Review"
            type="datetime-local"
            value={editProgress?.next_review || ""}
            onChange={(e) =>
              setEditProgress({ ...editProgress, next_review: e.target.value })
            }
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Streak"
            type="number"
            value={editProgress?.streak || 0}
            onChange={(e) =>
              setEditProgress({ ...editProgress, streak: parseInt(e.target.value) })
            }
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Ease Factor"
            type="number"
            value={editProgress?.ease_factor || 2.5}
            onChange={(e) =>
              setEditProgress({ ...editProgress, ease_factor: parseFloat(e.target.value) })
            }
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Interval"
            type="number"
            value={editProgress?.interval || 1}
            onChange={(e) =>
              setEditProgress({ ...editProgress, interval: parseInt(e.target.value) })
            }
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEditDialog(false)}>Cancel</Button>
          <Button onClick={handleUpdateProgress} color="primary">
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Progress;