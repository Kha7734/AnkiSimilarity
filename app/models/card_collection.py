# models/card_collection.py
import datetime
import eng_to_ipa as ipa
import nltk
from nltk.corpus import wordnet
from transformers import pipeline
from gtts import gTTS
import os
from flask import current_app

# Download WordNet data (only needed once)
nltk.download('wordnet')

class VocabularyCard:
    def __init__(self, card_id, user_id, dataset_id, word, meaning_en, meaning_vi,
                 ipa_transcription, example_sentences_en, example_sentences_vi,
                 visual_image_url, audio_url_word, audio_url_example1, audio_url_example2,
                 synonyms, antonyms, created_at=None, updated_at=None):
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
        self.audio_url_word = audio_url_word  # Audio for the word
        self.audio_url_example1 = audio_url_example1  # Audio for the first example sentence
        self.audio_url_example2 = audio_url_example2  # Audio for the second example sentence
        self.synonyms = synonyms
        self.antonyms = antonyms
        self.created_at = created_at if created_at else datetime.datetime.now()
        self.updated_at = updated_at if updated_at else datetime.datetime.now()

    @staticmethod
    def create_card(user_id, dataset_id, word, meaning_en=None, meaning_vi=None,
                    ipa_transcription=None, example_sentences_en=None, example_sentences_vi=None,
                    visual_image_url=None):
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
            antonyms
        )

        # Save to database to get the card_id
        result = current_app.db.vocabulary_cards.insert_one(new_card.__dict__)
        new_card.card_id = str(result.inserted_id)

        # Generate audio files with card_id in the filename
        audio_dir = "audio_files"  # Directory to store audio files
        os.makedirs(audio_dir, exist_ok=True)  # Create directory if it doesn't exist

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

    # Load a pre-trained GPT-2 model for text generation
    generator = pipeline('text-generation', model='gpt2', device='cuda')

    @staticmethod
    def get_example_sentences(word):
        prompt = f"The word '{word}' can be used in a sentence as follows:"
        generated_text = VocabularyCard.generator(prompt, max_length=150, num_return_sequences=1)
        return [generated_text[0]['generated_text']]

    @staticmethod
    def get_meaning_en(word):
        # Prompt for generating English meaning
        prompt = f"Provide a concise definition of the word '{word}' in English: (only provide meaning, nothing else)"
        generated_text = VocabularyCard.generator(prompt, max_length=150, num_return_sequences=1)

        # Extract only the definition (remove the prompt and extra text)
        definition = generated_text[0]['generated_text'].replace(prompt, "").strip()
        return definition

    @staticmethod
    def get_meaning_vi(word):
        # Prompt for generating Vietnamese meaning
        prompt = f"Hãy cung cấp nghĩa tiếng Việt của từ {word}: (Chỉ cung cấp nghĩa thôi)"
        generated_text = VocabularyCard.generator(prompt, max_length=150, num_return_sequences=1)

        # Extract only the definition (remove the prompt and extra text)
        definition = generated_text[0]['generated_text'].replace(prompt, "").strip()
        return definition