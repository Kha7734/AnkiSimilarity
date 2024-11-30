# AnkiSimilarity

## Introduction to this App

- I want to build an app to learn English vocabulary based on the idea of Anki Application. 
- Main features for learning English vocabulary: 
  1. Meaning: Get the meaning of vocabulary in both Vietnamese and English languages; Synonym and antonym in English
  2. Example Sentences: This app provide 2 example sentences in 2 different situation
  3. Visualize Images: This app provide images to easy in understanding and remembering the vocabulary
  4. Voice: This app provide speech of vocabulary and example sentences.

- This app is simple, easy to use, light and sharp. 
- This app is built on Python and some suitable AI model to handle some features. 
- The code should be built in way that application could update and integrate new features without make a large affect to current features.
- The backbone algorithm of this app is using active recall and space repetition to learn and practice new vocabulary

## Features Detail
This app has 2 main fields: learning and creating new database
### Learning Fields:

#### Learn a card:
1. The database will be created into many cards of vocabulary. Each card has 2 parts: guessing and meaning.
  - The guessing part:
    - There are some hints for user to guess the vocabulary: number of character in this words, the first char or some hints chars; the mearning in English; Visualize images. 
    - User will follow hints to guess the correct vocabulary. There is a input part for user to typing their guess.

  - The Back part of card:
    - Here, user could see all things that this card stores: The meaning, the visualize image, the example sentences, IPA of this words, speech of this word and speech of example sentences. The speech will be automatic played started by IPA then example sentences. This should have a play button for IPA, 2 examples to re-play.
    - Then, user could choose how long this vocabulary should be appear based on the theory of active recall and space repetition. The time-length is dynamic based on criteria: the first learn, practices or make a mistake when guessing.

#### CRUD database:
1. Create new database: User create a new database that stores many cards.
2. Read database: It used to learn or update database. 

In this CRUD database, user also could CRUD cards, the next part...

#### CRUD cards:
This is the main flow that make me to build this application
1. Create new card: A card has many fields: Meaning, Example sentences, Visualize images, IPA Speech and Example Speech.
- When creating new card, user will enter new English cards. After user enter english card, the application will do these following things:
  Using a tool or some suitable things to automate get these things:
    1. Get the meaning of this word in Vietnamese and English languages, the IPA. 
    2. Get 2 example sentences of this word in English in 2 different situation. Consider to embed a suitable LLM or language model that could generate 2 example in 2 sentences without using internet.
    3. Auto find a suitable image that user could imagine about this word based on image. The image gets on the Internet, so, when this feature requires Internet connection. This field also has a reload button, because the image is automate install, user could reload to find others.
    4. Speech: Based on the word and example sentences, this application should use a (fast, suitable model) to convert text-to-speech. This feature helps user listen to this word, how to spell and how to speak the example features. 

- This feature has some requirements: Becaused of storing and saving many fields, this features should use some technique to save images and audio of speech with less space requirement. 
