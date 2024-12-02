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


Updating the `README.md` file to document the user model flow is an important step for ensuring that other developers (or future you) can understand how to use the user management features of your AnkiSimilarity application. Below is a suggested structure and content for the `README.md` file, specifically focusing on the user model flow.

# Structure for README.md

```markdown
## User Model Flow

This section describes the user model functionality, including how to register, log in, update, retrieve, and delete users.

### 1. User Registration

**Endpoint**: `/register`  
**Method**: `POST`  
**Request Body**:
```json
{
    "username": "string",
    "email": "string",
    "password": "string"
}
```
- **Description**: This endpoint allows a new user to register for the application. It checks if the username and email already exist before creating a new user.
- **Response**:
  - **201 Created**: User created successfully.
  - **400 Bad Request**: Username or email already exists.

### 2. User Login

**Endpoint**: `/login`  
**Method**: `POST`  
**Request Body**:
```json
{
    "username": "string",
    "password": "string"
}
```
- **Description**: This endpoint allows an existing user to log in. It validates the username and password.
- **Response**:
  - **200 OK**: Login successful.
  - **401 Unauthorized**: Invalid username or password.

### 3. Get User Details

**Endpoint**: `/user/<user_id>`  
**Method**: `GET`  
- **Description**: This endpoint retrieves details of a specific user by their ID.
- **Response**:
  - **200 OK**: Returns user details.
  - **404 Not Found**: User not found.

### 4. Update User Details

**Endpoint**: `/user/<user_id>`  
**Method**: `PUT`  
**Request Body**:
```json
{
    "email": "string",        // Optional
    "password": "string"     // Optional
}
```
- **Description**: This endpoint updates specified fields (email, password) for a given user.
- **Response**:
  - **200 OK**: User updated successfully.

### 5. Delete User Account

**Endpoint**: `/user/<user_id>`  
**Method**: `DELETE`  
- **Description**: This endpoint deletes a user from the database based on their ID.
- **Response**:
  - **200 OK**: User deleted successfully.
  - **404 Not Found**: User not found.

## Database Connection

The application uses MongoDB as its database. Configuration settings are stored in `config.json`, which includes the MongoDB URI and database name. The password for the MongoDB connection is managed securely using a constant defined in `constant.py`.

## Testing

The application includes unit tests for the user model and routes, ensuring that all functionalities work as expected. Tests can be run using:
```bash
python -m unittest discover -s tests
```

## Conclusion

This README provides an overview of the user model flow within the AnkiSimilarity application. For further details on other features or components, please refer to additional sections in this document.
```

### Key Points to Include

1. **Overview of User Model Flow:** Briefly explain what functionalities are covered regarding user management.
2. **Endpoints:** Clearly document each API endpoint related to user operations (registration, login, retrieving user details, updating user information, and deleting users), including:
   - HTTP method
   - Request body format
   - Description of what each endpoint does
   - Possible responses with status codes
3. **Database Connection:** Mention how the application connects to MongoDB and where configuration settings are stored.
4. **Testing Information:** Provide instructions on how to run tests related to the user model and routes.
5. **Conclusion:** Summarize the importance of this section and encourage readers to explore other parts of the application.

By following this structure and content suggestions, you will create a comprehensive README.md file that effectively communicates how to use the user model features in your application. This documentation will be valuable for anyone working with your codebase in the future.