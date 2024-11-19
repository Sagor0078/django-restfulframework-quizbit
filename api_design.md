# API Design for Django RESTful Framework Quizbit

This document provides an overview of the API endpoints for the Django RESTful Framework Quizbit project.

## Authentication

### Obtain Token
- **URL:** `/api/token/`
- **Method:** `POST`
- **Description:** Obtain a JWT token for authentication.
- **Request Body:**
    ```json
    {
        "username": "string",
        "password": "string"
    }
    ```

- **Response:** 
  ```json
    {
    "access": "string",
    "refresh": "string"
    }

## Refresh Token
- **URL** : /api/token/refresh/
- **Method** : POST
- **Description** : Refresh the JWT token.
- **Request Body**:
```json
    {
        "refresh": "string"
    }
```
- **Response** :
```json
    {
    "access": "string"
    }
```
## Questions
- **List Questions**
- **URL** : /api/questions/
- **Method** : GET
- **Description** : Retrieve a list of quiz questions.
- **Respons** :
```json
[
  {
    "id": 1,
    "title": "string",
    "content": "string",
    "options": {
      "A": "string",
      "B": "string",
      "C": "string",
      "D": "string"
    },
    "correct_option": "A"
  }
]
```
## Retrieve Question
- **URL** : /api/questions/{id}/
- **Method** : GET
- **Description** : Retrieve details of a specific quiz question.
- **Response** :
```json
{
  "id": 1,
  "title": "string",
  "content": "string",
  "options": {
    "A": "string",
    "B": "string",
    "C": "string",
    "D": "string"
  },
  "correct_option": "A"
}
```

## Answers
- **Submit Answer**
- **URL** : /api/answers/
- **Method** : POST
- **Description** : Submit an answer to a quiz question.
- **Request Body** :
```json
{
  "question": 1,
  "selected_option": "A"
}
```
- **Response** :
```json
{
  "is_correct": true,
  "message": "Answer submitted successfully!"
}
```

## Practice History
- **Retrieve Practice History**
- **URL** : /api/history/
- **Method** : GET
- **Description** : Retrieve the practice history of the authenticated user.
- **Response**:
```json
{
  "user": 1,
  "total_questions": 10,
  "correct_answers": 8,
  "last_practiced": "2024-11-17T05:31:51Z"
}
```



## Notes
- All endpoints require JWT authentication unless specified otherwise.
- The selected_option in the Submit Answer endpoint should be one of the options provided in the question.
- The Retrieve Practice History endpoint returns the practice history of the authenticated user.
- This document provides a high-level overview of the API endpoints. For detailed API documentation, refer to the Swagger or Redoc documentation available at /swagger/ and /redoc/ respectively.








