import datetime
import eng_to_ipa as ipa
import nltk
from nltk.corpus import wordnet
from gtts import gTTS
import os
import requests
import json
from flask import current_app

# Download WordNet data (only needed once)
nltk.download('wordnet')

class VocabularyCard:
    def __init__(self, card_id, user_id, dataset_id, word, meaning_en, meaning_vi,
                 ipa_transcription, example_sentences_en, example_sentences_vi,
                 visual_image_url, audio_url_word, audio_url_example1, audio_url_example2,
                 synonyms, antonyms, word_type=None, vocab_family=None, created_at=None, updated_at=None):
        self.card_id = card_id
        self.user_id = user_id
        self.dataset_id = dataset_id
        self.word = word
        self.meaning_en = meaning_en
        self.meaning_vi = meaning_vi
        self.ipa_transcription = ipa_transcription
        self.example_sentences_en = example_sentences_en
        self.example_sentences_vi = example_sentences_vi
        self.visual_image_url = visual_image_url
        self.audio_url_word = audio_url_word
        self.audio_url_example1 = audio_url_example1
        self.audio_url_example2 = audio_url_example2
        self.synonyms = synonyms
        self.antonyms = antonyms
        self.word_type = word_type  # New field: word type (e.g., noun, verb, adjective)
        self.vocab_family = vocab_family  # New field: vocabulary family (related words)
        self.created_at = created_at if created_at else datetime.datetime.now()
        self.updated_at = updated_at if updated_at else datetime.datetime.now()

    @staticmethod
    def query_lm_studio(prompt, max_tokens=100):
        """
        Sends a prompt to the LM Studio server and returns the generated text.
        """
        url = "http://localhost:1234/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Error querying LM Studio: {e}")
            return None

    @staticmethod
    def get_word_type(word):
        """
        Determines the word type (e.g., noun, verb, adjective) using the LM Studio server.
        """
        prompt = f"What is the word type (part of speech) of the word '{word}'? Provide only the word type, nothing else."
        return VocabularyCard.query_lm_studio(prompt)

    @staticmethod
    def get_vocab_family(word):
        """
        Generates a list of related words or word forms (vocabulary family) using the LM Studio server.
        Specifically requests related words in different grammatical forms (noun, verb, adjective, etc.).
        Returns the list in the format:
        1. Word (form)
        2. Word (form)
        ...
        """
        prompt = (
            f"Provide a list of related words or word forms for the word '{word}' in different grammatical forms "
            "(e.g., noun, verb, adjective, adverb). Format the response as a numbered list, with each word followed by its grammatical form in parentheses. "
            "Example:\n"
            "1. Exaggeration (noun)\n"
            "2. Exaggerated (adjective)\n"
            "3. Exaggeratedly (adverb)\n"
            "Provide only the numbered list, nothing else."
        )
        return VocabularyCard.query_lm_studio(prompt, max_tokens=100)

    @staticmethod
    def get_meaning_en(word):
        """
        Generates the English meaning of a word in multiple contexts using the LM Studio server.
        Returns a list of meanings with examples or contexts.
        """
        prompt = (
            f"Provide the meaning of the word '{word}' in English, including different contexts or usages. "
            "For each meaning, include a brief explanation or example sentence in English. "
            "Format the response as a numbered list, like this:\n"
            "1. Meaning 1 (Context/Explanation)\n"
            "   - Example sentence in English.\n"
            "2. Meaning 2 (Context/Explanation)\n"
            "   - Example sentence in English.\n"
            "Provide only the numbered list, nothing else."
        )
        return VocabularyCard.query_lm_studio(prompt, max_tokens=200)

    @staticmethod
    def get_meaning_vi(word):
        """
        Translates a word from English to Vietnamese and provides its meaning in multiple contexts using the LM Studio server.
        Returns a list of meanings with examples or contexts.
        """
        prompt = (
            f"Translate the word '{word}' from English to Vietnamese and provide its meaning in different contexts or usages. "
            "For each meaning, include a brief explanation or example sentence in Vietnamese. "
            "Format the response as a numbered list, like this:\n"
            "1. Meaning 1 (Context/Explanation)\n"
            "   - Example sentence in Vietnamese.\n"
            "2. Meaning 2 (Context/Explanation)\n"
            "   - Example sentence in Vietnamese.\n"
            "Provide only the numbered list, nothing else."
        )
        return VocabularyCard.query_lm_studio(prompt, max_tokens=200)

    @staticmethod
    def get_example_sentences(word):
        """
        Generates example sentences using the word with the LM Studio server.
        """
        prompt = f"Write two clear and grammatically correct example sentences using the word '{word}' in English. Do not include definitions or explanations."
        examples = VocabularyCard.query_lm_studio(prompt, max_tokens=200)
        if examples:
            print(f'Examples: {examples}')
            return examples.split("\n")
        return ["Example sentence not available."]

    @staticmethod
    def create_card(user_id, dataset_id, word, meaning_en=None, meaning_vi=None,
                    ipa_transcription=None, example_sentences_en=None, example_sentences_vi=None,
                    visual_image_url=None, word_type=None, vocab_family=None):
        try:
            # Automatically generate IPA transcription if not provided
            if not ipa_transcription:
                ipa_transcription = VocabularyCard.get_ipa_transcription(word)

            # Automatically generate synonyms and antonyms
            synonyms, antonyms = VocabularyCard.get_synonyms_antonyms(word)

            # Automatically generate example sentences if not provided
            if not example_sentences_en:
                example_sentences_en = VocabularyCard.get_example_sentences(word)

            # Automatically generate English meaning if not provided
            if not meaning_en:
                meaning_en = VocabularyCard.get_meaning_en(word)

            # Automatically generate Vietnamese meaning if not provided
            if not meaning_vi:
                meaning_vi = VocabularyCard.get_meaning_vi(word)

            # Automatically generate word type if not provided
            if not word_type:
                word_type = VocabularyCard.get_word_type(word)

            # Automatically generate vocabulary family if not provided
            if not vocab_family:
                vocab_family = VocabularyCard.get_vocab_family(word)

            # Create a temporary card to get the card_id
            new_card = VocabularyCard(
                None,
                user_id,
                dataset_id,
                word,
                meaning_en,
                meaning_vi,
                ipa_transcription,
                example_sentences_en,
                example_sentences_vi,
                visual_image_url,
                None,  # audio_url_word (will be generated later)
                None,  # audio_url_example1 (will be generated later)
                None,  # audio_url_example2 (will be generated later)
                synonyms,
                antonyms,
                word_type,  # New field: word type
                vocab_family  # New field: vocabulary family
            )

            # Save to database to get the card_id
            result = current_app.db.vocabulary_cards.insert_one(new_card.__dict__)
            new_card.card_id = str(result.inserted_id)

            # Generate audio files with card_id in the filename
            audio_dir = "audio_files"
            os.makedirs(audio_dir, exist_ok=True)

            # Generate audio for the word
            audio_url_word = VocabularyCard.generate_speech(
                new_card.word,
                os.path.join(audio_dir, f"audio_word_{new_card.card_id}.mp3")
            )

            # Generate audio for the first example sentence
            audio_url_example1 = VocabularyCard.generate_speech(
                new_card.example_sentences_en[0],
                os.path.join(audio_dir, f"audio_example1_{new_card.card_id}.mp3")
            )

            # Generate audio for the second example sentence
            audio_url_example2 = VocabularyCard.generate_speech(
                new_card.example_sentences_en[1],
                os.path.join(audio_dir, f"audio_example2_{new_card.card_id}.mp3")
            )

            # Update the card with the generated audio URLs
            new_card.audio_url_word = audio_url_word
            new_card.audio_url_example1 = audio_url_example1
            new_card.audio_url_example2 = audio_url_example2

            # Update the card in the database with the new audio URLs
            current_app.db.vocabulary_cards.update_one(
                {"_id": result.inserted_id},
                {"$set": {
                    "card_id": new_card.card_id,
                    "audio_url_word": audio_url_word,
                    "audio_url_example1": audio_url_example1,
                    "audio_url_example2": audio_url_example2
                }}
            )

            return new_card
        except Exception as e:
            print(f"Error creating card: {e}")
            return None

    # Other methods (get_card_by_id, update_card, delete_card, etc.) remain unchanged
    @staticmethod
    def get_card_by_id(card_id):
        return current_app.db.vocabulary_cards.find_one({"card_id": card_id})

    @staticmethod
    def update_card(card_id, update_fields):
        update_fields['updated_at'] = datetime.datetime.now()  # Update timestamp on modification
        current_app.db.vocabulary_cards.update_one({"card_id": card_id}, {"$set": update_fields})

    @staticmethod
    def delete_card(card_id):
        # Delete associated audio files
        audio_dir = "audio_files"
        for filename in [
            f"audio_word_{card_id}.mp3",
            f"audio_example1_{card_id}.mp3",
            f"audio_example2_{card_id}.mp3"
        ]:
            file_path = os.path.join(audio_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Delete the card from the database
        current_app.db.vocabulary_cards.delete_one({"card_id": card_id})

    @staticmethod
    def get_cards_by_user(user_id):
        return list(current_app.db.vocabulary_cards.find({"user_id": user_id}))

    @staticmethod
    def get_cards_by_dataset(dataset_id):
        return list(current_app.db.vocabulary_cards.find({"dataset_id": dataset_id}))

    @staticmethod
    def get_ipa_transcription(word):
        return ipa.convert(word)

    @staticmethod
    def get_synonyms_antonyms(word):
        synonyms = set()
        antonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
                if lemma.antonyms():
                    antonyms.add(lemma.antonyms()[0].name())
        return list(synonyms), list(antonyms)

    @staticmethod
    def generate_speech(text, filepath):
        tts = gTTS(text=text, lang='en')
        tts.save(filepath)
        return filepath