import React, { useEffect, useState } from "react";
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from "@mui/material";
import { useAuth } from "../AuthContext"; // Import useAuth
import {
  fetchDatasets,
  createDataset,
  updateDataset,
  deleteDataset,
} from "../services/api"; // Import external functions

const Datasets = () => {
  const [datasets, setDatasets] = useState([]);
  const [newDatasetName, setNewDatasetName] = useState("");
  const [newDatasetDescription, setNewDatasetDescription] = useState("");
  const [editDataset, setEditDataset] = useState(null);
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const { user } = useAuth(); // Get the authenticated user from context

  // Fetch datasets created by the user
  useEffect(() => {
    if (user) {
      const loadDatasets = async () => {
        try {
          const data = await fetchDatasets(user._id); // Use external function
          setDatasets(data);
        } catch (error) {
          console.error("Error loading datasets:", error);
        }
      };

      loadDatasets();
    }
  }, [user]);

  // Add a new dataset
  const handleAddDataset = async () => {
    if (!user) return; // Ensure the user is authenticated
    try {
      const newDataset = await createDataset(
        user._id,
        newDatasetName,
        newDatasetDescription
      ); // Use external function
      setDatasets([...datasets, newDataset]);
      setNewDatasetName("");
      setNewDatasetDescription("");
    } catch (error) {
      console.error("Error adding dataset:", error);
    }
  };

  // Open edit dialog for a dataset
  const handleEditDataset = (dataset) => {
    setEditDataset(dataset);
    setOpenEditDialog(true);
  };

  // Update a dataset
  const handleUpdateDataset = async () => {
    try {
      const updatedDataset = await updateDataset(
        editDataset._id,
        editDataset.name,
        editDataset.description
      ); // Use external function
      setDatasets(
        datasets.map((dataset) =>
          dataset._id === editDataset._id ? updatedDataset : dataset
        )
      );
      setOpenEditDialog(false);
    } catch (error) {
      console.error("Error updating dataset:", error);
    }
  };

  // Delete a dataset
  const handleDeleteDataset = async (datasetId) => {
    try {
      await deleteDataset(datasetId); // Use external function
      setDatasets(datasets.filter((dataset) => dataset._id !== datasetId));
    } catch (error) {
      console.error("Error deleting dataset:", error);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Dataset Management
      </Typography>

      {/* Add New Dataset Form */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Dataset Name"
            value={newDatasetName}
            onChange={(e) => setNewDatasetName(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Dataset Description"
            value={newDatasetDescription}
            onChange={(e) => setNewDatasetDescription(e.target.value)}
          />
        </Grid>
        <Grid item xs={12}>
          <Button variant="contained" color="primary" onClick={handleAddDataset}>
            Add Dataset
          </Button>
        </Grid>
      </Grid>

      {/* Datasets List */}
      <Grid container spacing={3}>
        {datasets.map((dataset) => (
          <Grid item xs={12} md={6} key={dataset._id}>
            <Card>
              <CardContent>
                <Typography variant="h6">{dataset.name}</Typography>
                <Typography variant="body1">{dataset.description}</Typography>
                <Typography variant="body2" color="textSecondary">
                  Created: {new Date(dataset.created_at).toLocaleDateString()}
                </Typography>
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={() => handleEditDataset(dataset)}
                >
                  Edit
                </Button>
                <Button
                  variant="outlined"
                  color="secondary"
                  onClick={() => handleDeleteDataset(dataset._id)}
                >
                  Delete
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Edit Dataset Dialog */}
      <Dialog open={openEditDialog} onClose={() => setOpenEditDialog(false)}>
        <DialogTitle>Edit Dataset</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Dataset Name"
            value={editDataset?.name || ""}
            onChange={(e) =>
              setEditDataset({ ...editDataset, name: e.target.value })
            }
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Dataset Description"
            value={editDataset?.description || ""}
            onChange={(e) =>
              setEditDataset({ ...editDataset, description: e.target.value })
            }
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEditDialog(false)}>Cancel</Button>
          <Button onClick={handleUpdateDataset} color="primary">
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Datasets;