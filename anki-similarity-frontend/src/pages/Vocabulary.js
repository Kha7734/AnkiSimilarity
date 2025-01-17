import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
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
    CircularProgress,
    Snackbar,
    Alert,
    Chip,
    Box,
} from "@mui/material";
import {useAuth} from "../AuthContext";
import {
    fetchVocabularyCards,
    createVocabularyCard,
    updateVocabularyCard,
    deleteVocabularyCard,
} from "../services/api";

const Vocabulary = () => {
    const {datasetId} = useParams();
    const [vocabularyCards, setVocabularyCards] = useState([]);
    const [newWord, setNewWord] = useState("");
    const [newMeaningEn, setNewMeaningEn] = useState("");
    const [newMeaningVi, setNewMeaningVi] = useState("");
    const [ipaTranscription, setIpaTranscription] = useState("");
    const [exampleSentences, setExampleSentences] = useState([]);
    const [synonyms, setSynonyms] = useState([]);
    const [antonyms, setAntonyms] = useState([]);
    const [wordType, setWordType] = useState("");
    const [vocabFamily, setVocabFamily] = useState([]);
    const [editCard, setEditCard] = useState(null);
    const [openEditDialog, setOpenEditDialog] = useState(false);
    const {user} = useAuth();

    const [isGenerating, setIsGenerating] = useState(false);
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState("");
    const [snackbarSeverity, setSnackbarSeverity] = useState("success");
    const [audioBase64, setAudioBase64] = useState("");

    // Fetch vocabulary cards
    useEffect(() => {
        const loadVocabularyCards = async () => {
            try {
                const data = await fetchVocabularyCards(datasetId);
                setVocabularyCards(data);
            } catch (error) {
                console.error("Error loading vocabulary cards:", error);
            }
        };

        loadVocabularyCards();
    }, [datasetId]);

    // Add a new vocabulary card
    const handleAddCard = async () => {
        if (!user) return;

        try {
            console.log("User:", user); // Debugging line
            const newCard = await createVocabularyCard(
                user._id,
                datasetId,
                newWord,
                newMeaningEn,
                newMeaningVi,
                ipaTranscription,
                exampleSentences,
                [], // example_sentences_vi
                "", // visual_image_url
                "", // audio_url_word
                "", // audio_url_example
                wordType, // New field: word type
                vocabFamily // New field: vocabulary family
            );

            // Update the vocabulary cards list
            setVocabularyCards([...vocabularyCards, newCard]);

            // Clear the form fields
            setNewWord("");
            setNewMeaningEn("");
            setNewMeaningVi("");
            setIpaTranscription("");
            setExampleSentences([]);
            setSynonyms([]);
            setAntonyms([]);
            setWordType("");
            setVocabFamily([]);
            setAudioBase64(""); // Clear audio data

            // Show success message in the snackbar
            setSnackbarMessage("Vocabulary card added successfully!");
            setSnackbarSeverity("success");
            setSnackbarOpen(true);
        } catch (error) {
            console.error("Error adding vocabulary card:", error);

            // Show error message in the snackbar
            setSnackbarMessage("Failed to add vocabulary card. Please try again.");
            setSnackbarSeverity("error");
            setSnackbarOpen(true);
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
                editCard.meaning_vi,
                editCard.ipa_transcription,
                editCard.example_sentences_en,
                editCard.synonyms,
                editCard.antonyms,
                editCard.word_type, // New field: word type
                editCard.vocab_family // New field: vocabulary family
            );
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
            await deleteVocabularyCard(cardId);
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

        setIsGenerating(true);

        try {
            const response = await fetch("/cards/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({word: newWord}),
            });

            if (!response.ok) {
                throw new Error("Failed to generate fields");
            }

            const data = await response.json();
            console.log("Generated Data:", data);

            // Ensure vocab_family is an array
            const vocabFamilyArray = Array.isArray(data.vocab_family)
                ? data.vocab_family
                : data.vocab_family
                    ? [data.vocab_family]
                    : [];

            setNewMeaningEn(data.meaning_en || "");
            setNewMeaningVi(data.meaning_vi || "");
            setIpaTranscription(data.ipa_transcription || "");
            setSynonyms(data.synonyms || []);
            setAntonyms(data.antonyms || []);
            setExampleSentences(data.example_sentences_en || []);
            setWordType(data.word_type || "");
            setVocabFamily(vocabFamilyArray); // Ensure vocabFamily is always an array
            setAudioBase64(data.audio_base64 || ""); // Set the base64 audio data

            setSnackbarMessage("Fields generated successfully!");
            setSnackbarSeverity("success");
            setSnackbarOpen(true);
        } catch (error) {
            console.error("Error generating fields:", error);
            setSnackbarMessage("Failed to generate fields. Please try again.");
            setSnackbarSeverity("error");
            setSnackbarOpen(true);
        } finally {
            setIsGenerating(false);
        }
    };


    // Close the snackbar
    const handleCloseSnackbar = () => {
        setSnackbarOpen(false);
    };

    // Color mapping for word types
    const wordTypeColors = {
        noun: "primary",
        verb: "success",
        adjective: "warning",
        adverb: "error",
        other: "default",
    };

    // Get the color for the word type
    const getWordTypeColor = (type) => {
        return wordTypeColors[type.toLowerCase()] || "default";
    };

    // Function to play audio from base64 data
    const playAudio = (audioBase64) => {
        if (audioBase64) {
            const audioSrc = `data:audio/mp3;base64,${audioBase64}`;
            const audio = new Audio(audioSrc);
            audio.play().catch((error) => {
                console.error("Error playing audio:", error);
            });
        } else {
            console.error("No audio data provided.");
        }
    };

    return (
        <Container>
            <Typography variant="h4" gutterBottom>
                Vocabulary List
            </Typography>

            {/* Add New Vocabulary Card Form */}
            <Grid container spacing={2} sx={{mb: 4}}>
                {/* Group 1: Vocabulary, IPA, Synonyms, Antonyms */}
                <Grid item xs={12} container spacing={2}>
                    <Grid item xs={12} md={3}>
                        <Box>
                            <TextField
                                fullWidth
                                label="New Word"
                                value={newWord}
                                onChange={(e) => setNewWord(e.target.value)}
                                sx={{
                                    "& .MuiInputBase-input": {
                                        color: getWordTypeColor(wordType), // Change text color based on word type
                                    },
                                }}
                            />
                            {wordType && (
                                <Typography variant="caption" sx={{mt: 1, display: "block"}}>
                                    Word Type:{" "}
                                    <Chip
                                        label={wordType}
                                        color={getWordTypeColor(wordType)}
                                        size="small"
                                    />
                                </Typography>
                            )}
                        </Box>
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
                            value={synonyms.join(", ")}
                            onChange={(e) => setSynonyms(e.target.value.split(", "))}
                        />
                    </Grid>
                    <Grid item xs={12} md={3}>
                        <TextField
                            fullWidth
                            label="Antonyms"
                            value={antonyms.join(", ")}
                            onChange={(e) => setAntonyms(e.target.value.split(", "))}
                        />
                    </Grid>
                </Grid>

                {/* Group 2: Meaning (English) and Meaning (Vietnamese) */}
                <Grid item xs={12} container spacing={2}>
                    {/* Meaning (English) */}
                    <Grid item xs={12} md={6}>
                        <Typography variant="h6" gutterBottom>
                            Meaning (English)
                        </Typography>
                        <Box
                            sx={{
                                border: "1px solid #ccc",
                                borderRadius: "4px",
                                padding: "16px",
                                backgroundColor: "#f9f9f9",
                                maxHeight: "200px",
                                overflowY: "auto",
                            }}
                        >
                            {newMeaningEn.split("\n").map((line, index) => (
                                <div key={index}>
                                    {line.startsWith("1.") || line.startsWith("2.") || line.startsWith("3.") ? (
                                        <Typography variant="body1" component="div">
                                            <strong>{line.split(" ")[0]}</strong> {line.split(" ").slice(1).join(" ")}
                                        </Typography>
                                    ) : (
                                        <Typography variant="body1" component="div">
                                            {line}
                                        </Typography>
                                    )}
                                </div>
                            ))}
                        </Box>
                    </Grid>

                    {/* Meaning (Vietnamese) */}
                    <Grid item xs={12} md={6}>
                        <Typography variant="h6" gutterBottom>
                            Meaning (Vietnamese)
                        </Typography>
                        <Box
                            sx={{
                                border: "1px solid #ccc",
                                borderRadius: "4px",
                                padding: "16px",
                                backgroundColor: "#f9f9f9",
                                maxHeight: "200px",
                                overflowY: "auto",
                            }}
                        >
                            {newMeaningVi.split("\n").map((line, index) => (
                                <div key={index}>
                                    {line.startsWith("1.") || line.startsWith("2.") || line.startsWith("3.") ? (
                                        <Typography variant="body1" component="div">
                                            <strong>{line.split(" ")[0]}</strong> {line.split(" ").slice(1).join(" ")}
                                        </Typography>
                                    ) : (
                                        <Typography variant="body1" component="div">
                                            {line}
                                        </Typography>
                                    )}
                                </div>
                            ))}
                        </Box>
                    </Grid>
                </Grid>

                {/* Example Sentences */}
                <Grid item xs={12}>
                    <TextField
                        fullWidth
                        label="Example Sentences"
                        value={exampleSentences.join("\n")}
                        onChange={(e) => setExampleSentences(e.target.value.split("\n"))}
                        multiline
                        rows={6}
                    />
                </Grid>

                {/* Buttons */}
                <Grid item xs={12} container justifyContent="flex-end">
                    <Button
                        variant="contained"
                        color="secondary"
                        onClick={handleGenerateFields}
                        disabled={isGenerating}
                        sx={{mr: 2}} // Add margin to the right for spacing
                    >
                        {isGenerating ? <CircularProgress size={24}/> : "Generate Fields"}
                    </Button>
                    <Button variant="contained" color="primary" onClick={handleAddCard} sx={{mr: 2}}>
                        Add Card
                    </Button>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={() => playAudio(audioBase64)}
                        disabled={!audioBase64}
                    >
                        Play Word Audio
                    </Button>
                </Grid>
            </Grid>

            {/* Vocabulary Cards List */}
            <Grid container spacing={3}>
                {vocabularyCards.map((card) => (
                    <Grid item xs={12} md={6} key={card.card_id}>
                        <Card>
                            <CardContent>
                                {/* Word and Word Type */}
                                <Typography variant="h6">
                                    {card.word}{" "}
                                    <Chip
                                        label={card.word_type}
                                        color={getWordTypeColor(card.word_type)}
                                        size="small"
                                    />
                                </Typography>
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
                                    <strong>Vocabulary Family:</strong>{" "}
                                    {card.vocab_family?.join(", ")}
                                </Typography>
                                <Typography variant="body1">
                                    <strong>Example Sentences:</strong>
                                    <ul>
                                        {card.example_sentences_en?.map((sentence, index) => (
                                            <li key={index}>{sentence}</li>
                                        ))}
                                    </ul>
                                </Typography>

                                {/* Play Audio Buttons */}
                                <Box sx={{mt: 2}}>
                                    <Button
                                        variant="outlined"
                                        color="primary"
                                        onClick={() => playAudio(card.audio_url_word)}
                                        sx={{mr: 2}}
                                    >
                                        Play Word Audio
                                    </Button>
                                    <Button
                                        variant="outlined"
                                        color="secondary"
                                        onClick={() => playAudio(card.audio_url_example1)}
                                        sx={{mr: 2}}
                                    >
                                        Play Example 1 Audio
                                    </Button>
                                    <Button
                                        variant="outlined"
                                        color="success"
                                        onClick={() => playAudio(card.audio_url_example2)}
                                    >
                                        Play Example 2 Audio
                                    </Button>
                                </Box>

                                {/* Edit and Delete Buttons */}
                                <Box sx={{mt: 2}}>
                                    <Button
                                        variant="outlined"
                                        color="primary"
                                        onClick={() => handleEditCard(card)}
                                        sx={{mr: 2}}
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
                                </Box>
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
                        onChange={(e) => setEditCard({...editCard, word: e.target.value})}
                        sx={{mb: 2}}
                    />
                    <TextField
                        fullWidth
                        label="Meaning (English)"
                        value={editCard?.meaning_en || ""}
                        onChange={(e) =>
                            setEditCard({...editCard, meaning_en: e.target.value})
                        }
                        multiline
                        rows={4}
                        sx={{mb: 2}}
                    />
                    <TextField
                        fullWidth
                        label="Meaning (Vietnamese)"
                        value={editCard?.meaning_vi || ""}
                        onChange={(e) =>
                            setEditCard({...editCard, meaning_vi: e.target.value})
                        }
                        multiline
                        rows={4}
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
                    sx={{width: "100%"}}
                >
                    {snackbarMessage}
                </Alert>
            </Snackbar>
        </Container>
    );
};

export default Vocabulary;