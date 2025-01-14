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
  CircularProgress, // Add CircularProgress for loading spinner
  Snackbar, // Add Snackbar for success/error feedback
  Alert, // Add Alert for Snackbar messages
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
  const [ipaTranscription, setIpaTranscription] = useState("");
  const [exampleSentences, setExampleSentences] = useState([]);
  const [synonyms, setSynonyms] = useState([]);
  const [antonyms, setAntonyms] = useState([]);
  const [editCard, setEditCard] = useState(null); // Card being edited
  const [openEditDialog, setOpenEditDialog] = useState(false); // Edit dialog state
  const { user } = useAuth(); // Get the authenticated user from context

  // Loading state for generating fields
  const [isGenerating, setIsGenerating] = useState(false);

  // Snackbar state for success/error feedback
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] = useState("success"); // "success" or "error"

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
        newMeaningVi,
        ipaTranscription,
        exampleSentences,
        [], // example_sentences_vi (optional)
        "", // visual_image_url (optional)
        "", // audio_url_word (optional)
        "" // audio_url_example (optional)
      ); // Use external function
      setVocabularyCards([...vocabularyCards, newCard]);
      setNewWord("");
      setNewMeaningEn("");
      setNewMeaningVi("");
      setIpaTranscription("");
      setExampleSentences([]);
      setSynonyms([]);
      setAntonyms([]);
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

  // Generate fields automatically
  const handleGenerateFields = async () => {
    if (!newWord) {
      alert("Please enter a word first.");
      return;
    }

    setIsGenerating(true); // Start loading

    try {
      const response = await fetch("/cards/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ word: newWord }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate fields");
      }

      const data = await response.json();
      console.log("Generated Data:", data); // Log the data to verify

      // Populate the form fields with the generated data
      setNewMeaningEn(data.meaning_en || ""); // Update English meaning
      setNewMeaningVi(data.meaning_vi || ""); // Update Vietnamese meaning
      setIpaTranscription(data.ipa_transcription || "");
      setSynonyms(data.synonyms || []);
      setAntonyms(data.antonyms || []);
      setExampleSentences(data.example_sentences_en || []);

      // Show success feedback
      setSnackbarMessage("Fields generated successfully!");
      setSnackbarSeverity("success");
      setSnackbarOpen(true);
    } catch (error) {
      console.error("Error generating fields:", error);

      // Show error feedback
      setSnackbarMessage("Failed to generate fields. Please try again.");
      setSnackbarSeverity("error");
      setSnackbarOpen(true);
    } finally {
      setIsGenerating(false); // Stop loading
    }
  };

  // Close the snackbar
  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Vocabulary List
      </Typography>

      {/* Add New Vocabulary Card Form */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        {/* Group 1: Vocabulary, IPA, Synonyms, Antonyms */}
        <Grid item xs={12} container spacing={2}>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="New Word"
              value={newWord}
              onChange={(e) => setNewWord(e.target.value)}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="IPA Transcription"
              value={ipaTranscription}
              onChange={(e) => setIpaTranscription(e.target.value)}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="Synonyms"
              value={synonyms.join(", ")} // Display synonyms as a comma-separated string
              onChange={(e) => setSynonyms(e.target.value.split(", "))}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="Antonyms"
              value={antonyms.join(", ")} // Display antonyms as a comma-separated string
              onChange={(e) => setAntonyms(e.target.value.split(", "))}
            />
          </Grid>
        </Grid>

        {/* Group 2: Meaning (English) and Meaning (Vietnamese) */}
        <Grid item xs={12} container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Meaning (English)"
              value={newMeaningEn}
              onChange={(e) => setNewMeaningEn(e.target.value)}
              multiline
              rows={4} // Increase rows for larger text input
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Meaning (Vietnamese)"
              value={newMeaningVi}
              onChange={(e) => setNewMeaningVi(e.target.value)}
              multiline
              rows={4} // Increase rows for larger text input
            />
          </Grid>
        </Grid>

        {/* Example Sentences */}
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Example Sentences"
            value={exampleSentences.join("\n")} // Display example sentences as newline-separated text
            onChange={(e) => setExampleSentences(e.target.value.split("\n"))}
            multiline
            rows={6} // Increase rows for larger text input
          />
        </Grid>

        {/* Buttons */}
        <Grid item xs={12}>
          <Button variant="contained" color="primary" onClick={handleAddCard}>
            Add Card
          </Button>
          <Button
            variant="contained"
            color="secondary"
            onClick={handleGenerateFields}
            disabled={isGenerating} // Disable button while generating
            sx={{ ml: 2 }}
          >
            {isGenerating ? <CircularProgress size={24} /> : "Generate Fields"}
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
                  <strong>IPA:</strong> {card.ipa_transcription}
                </Typography>
                <Typography variant="body1">
                  <strong>English:</strong> {card.meaning_en}
                </Typography>
                <Typography variant="body1">
                  <strong>Vietnamese:</strong> {card.meaning_vi}
                </Typography>
                <Typography variant="body1">
                  <strong>Synonyms:</strong> {card.synonyms?.join(", ")}
                </Typography>
                <Typography variant="body1">
                  <strong>Antonyms:</strong> {card.antonyms?.join(", ")}
                </Typography>
                <Typography variant="body1">
                  <strong>Example Sentences:</strong>
                  <ul>
                    {card.example_sentences_en?.map((sentence, index) => (
                      <li key={index}>{sentence}</li>
                    ))}
                  </ul>
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
            multiline
            rows={4} // Increase rows for larger text input
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Meaning (Vietnamese)"
            value={editCard?.meaning_vi || ""}
            onChange={(e) =>
              setEditCard({ ...editCard, meaning_vi: e.target.value })
            }
            multiline
            rows={4} // Increase rows for larger text input
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEditDialog(false)}>Cancel</Button>
          <Button onClick={handleUpdateCard} color="primary">
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for success/error feedback */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity={snackbarSeverity}
          sx={{ width: "100%" }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Vocabulary;