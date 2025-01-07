import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
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
  fetchVocabularyCards,
  createVocabularyCard,
  updateVocabularyCard,
  deleteVocabularyCard,
} from "../services/api"; // Import vocabulary card API functions

const Vocabulary = () => {
  const { datasetId } = useParams(); // Get dataset ID from URL
  const [vocabularyCards, setVocabularyCards] = useState([]);
  const [newWord, setNewWord] = useState("");
  const [newMeaningEn, setNewMeaningEn] = useState("");
  const [newMeaningVi, setNewMeaningVi] = useState("");
  const [editCard, setEditCard] = useState(null); // Card being edited
  const [openEditDialog, setOpenEditDialog] = useState(false); // Edit dialog state
  const { user } = useAuth(); // Get the authenticated user from context

  // Fetch vocabulary cards for the selected dataset
  useEffect(() => {
    const loadVocabularyCards = async () => {
      try {
        const data = await fetchVocabularyCards(datasetId); // Use external function
        setVocabularyCards(data);
      } catch (error) {
        console.error("Error loading vocabulary cards:", error);
      }
    };

    loadVocabularyCards();
  }, [datasetId]);

  // Add a new vocabulary card
  const handleAddCard = async () => {
    if (!user) return; // Ensure the user is authenticated
    try {
      const newCard = await createVocabularyCard(
        user._id,
        datasetId,
        newWord,
        newMeaningEn,
        newMeaningVi
      ); // Use external function
      setVocabularyCards([...vocabularyCards, newCard]);
      setNewWord("");
      setNewMeaningEn("");
      setNewMeaningVi("");
    } catch (error) {
      console.error("Error adding vocabulary card:", error);
    }
  };

  // Open edit dialog for a vocabulary card
  const handleEditCard = (card) => {
    setEditCard(card);
    setOpenEditDialog(true);
  };

  // Update a vocabulary card
  const handleUpdateCard = async () => {
    try {
      const updatedCard = await updateVocabularyCard(
        editCard.card_id,
        editCard.word,
        editCard.meaning_en,
        editCard.meaning_vi
      ); // Use external function
      setVocabularyCards(
        vocabularyCards.map((card) =>
          card.card_id === editCard.card_id ? updatedCard : card
        )
      );
      setOpenEditDialog(false);
    } catch (error) {
      console.error("Error updating vocabulary card:", error);
    }
  };

  // Delete a vocabulary card
  const handleDeleteCard = async (cardId) => {
    try {
      await deleteVocabularyCard(cardId); // Use external function
      setVocabularyCards(
        vocabularyCards.filter((card) => card.card_id !== cardId)
      );
    } catch (error) {
      console.error("Error deleting vocabulary card:", error);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Vocabulary List
      </Typography>

      {/* Add New Vocabulary Card Form */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="New Word"
            value={newWord}
            onChange={(e) => setNewWord(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Meaning (English)"
            value={newMeaningEn}
            onChange={(e) => setNewMeaningEn(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Meaning (Vietnamese)"
            value={newMeaningVi}
            onChange={(e) => setNewMeaningVi(e.target.value)}
          />
        </Grid>
        <Grid item xs={12}>
          <Button variant="contained" color="primary" onClick={handleAddCard}>
            Add Card
          </Button>
        </Grid>
      </Grid>

      {/* Vocabulary Cards List */}
      <Grid container spacing={3}>
        {vocabularyCards.map((card) => (
          <Grid item xs={12} md={6} key={card.card_id}>
            <Card>
              <CardContent>
                <Typography variant="h6">{card.word}</Typography>
                <Typography variant="body1">
                  <strong>English:</strong> {card.meaning_en}
                </Typography>
                <Typography variant="body1">
                  <strong>Vietnamese:</strong> {card.meaning_vi}
                </Typography>
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={() => handleEditCard(card)}
                >
                  Edit
                </Button>
                <Button
                  variant="outlined"
                  color="secondary"
                  onClick={() => handleDeleteCard(card.card_id)}
                >
                  Delete
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Edit Card Dialog */}
      <Dialog open={openEditDialog} onClose={() => setOpenEditDialog(false)}>
        <DialogTitle>Edit Vocabulary Card</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Word"
            value={editCard?.word || ""}
            onChange={(e) => setEditCard({ ...editCard, word: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Meaning (English)"
            value={editCard?.meaning_en || ""}
            onChange={(e) =>
              setEditCard({ ...editCard, meaning_en: e.target.value })
            }
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Meaning (Vietnamese)"
            value={editCard?.meaning_vi || ""}
            onChange={(e) =>
              setEditCard({ ...editCard, meaning_vi: e.target.value })
            }
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEditDialog(false)}>Cancel</Button>
          <Button onClick={handleUpdateCard} color="primary">
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Vocabulary;