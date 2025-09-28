# ZenithAI API Documentation

## Base URL
```
http://127.0.0.1:8000
```

## Authentication
All endpoints except registration and login require JWT authentication via Bearer token.

### Headers for authenticated requests
```
Authorization: Bearer <your_access_token>
```

## Endpoints

### Authentication

#### Register User
- **URL**: `POST /api/auth/register/`
- **Description**: Create a new user account
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "username": "username",
    "password": "password123",
    "password2": "password123"
  }
  ```
- **Success Response**: `201 Created`

#### Login
- **URL**: `POST /api/auth/token/`
- **Description**: Get JWT tokens
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "access": "jwt_token",
    "refresh": "refresh_token"
  }
  ```

#### Get User Profile
- **URL**: `GET /api/auth/profile/`
- **Authentication**: Required
- **Success Response**: `200 OK`

### Chat

#### List Conversations
- **URL**: `GET /api/chat/conversations/`
- **Authentication**: Required
- **Success Response**: `200 OK`

#### Create Conversation
- **URL**: `POST /api/chat/conversations/`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "title": "Conversation Title"
  }
  ```

#### Send Message
- **URL**: `POST /api/chat/chat/` (new conversation)
- **URL**: `POST /api/chat/chat/{conversation_id}/` (existing)
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "message": "Your message here"
  }
  ```

## Testing Flow

1. Register a user
2. Login to get tokens
3. Use access token for authenticated requests
4. Create a conversation
5. Send messages
6. View conversation history

## Postman Collection

- Import the collection file: `zenith-ai-api.postman_collection.json`
- Import the environment file: `zenith-ai-api.postman_environment.json`