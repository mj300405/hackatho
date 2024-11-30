# Authentication API Documentation

This document outlines the authentication endpoints and their usage for the hobby discovery application.

## Table of Contents
- [Registration](#registration)
- [Login](#login)
- [Token Refresh](#token-refresh)
- [User Details](#user-details)
- [Important Notes](#important-notes)

## Registration

**Endpoint:** `POST /api/register/`

### Request Body:
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "yourpassword123",
    "age": 25,
    "location": "Warsaw",
    "personality_type": "INTJ",
    "personality_details": {
        "introversion": 85,
        "intuition": 75,
        "thinking": 65,
        "judging": 55
    },
    "available_time": 60,
    "budget_preference": "MEDIUM"
}
```

### Success Response (200 OK):
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "age": 25,
    "location": "Warsaw",
    "personality_type": "INTJ",
    "personality_details": {
        "introversion": 85,
        "intuition": 75,
        "thinking": 65,
        "judging": 55
    },
    "available_time": 60,
    "budget_preference": "MEDIUM"
}
```

### Error Response (400 Bad Request):
```json
{
    "username": ["A user with that username already exists."],
    "email": ["Enter a valid email address."],
    "password": ["This password is too common."]
}
```

## Login

**Endpoint:** `POST /api/token/`

### Request Body:
```json
{
    "username": "testuser",
    "password": "yourpassword123"
}
```

### Success Response (200 OK):
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Error Response (401 Unauthorized):
```json
{
    "detail": "No active account found with the given credentials"
}
```

## Token Refresh

**Endpoint:** `POST /api/token/refresh/`

### Request Body:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Success Response (200 OK):
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Error Response (401 Unauthorized):
```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```

## User Details

**Endpoint:** `GET /api/user/`

### Request Headers:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Success Response (200 OK):
```json
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "age": 25,
    "location": "Warsaw",
    "personality_type": "INTJ",
    "available_time": 60,
    "budget_preference": "MEDIUM",
    "profile_completed": false,
    "coins": 0,
    "exp": 0
}
```

### Error Response (401 Unauthorized):
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Important Notes

### Authentication
- After successful login, store both access and refresh tokens
- Include access token in all authenticated requests in Authorization header
- Access token expires in 60 minutes
- Use refresh token to get new access token when needed

### Authorization Header Format
```javascript
headers: {
    'Authorization': 'Bearer your_access_token_here'
}
```

### Optional Registration Fields
- age
- location
- personality_type
- personality_details
- available_time
- budget_preference

### Error Handling
- 400 responses indicate validation errors
- 401 responses indicate authentication errors
- Implement token refresh logic when receiving 401 responses

### Personality Types
Available personality types for the `personality_type` field:
- INTJ - Architect
- INTP - Logician
- ENTJ - Commander
- ENTP - Debater
- INFJ - Advocate
- INFP - Mediator
- ENFJ - Protagonist
- ENFP - Campaigner
- ISTJ - Logistician
- ISFJ - Defender
- ESTJ - Executive
- ESFJ - Consul
- ISTP - Virtuoso
- ISFP - Adventurer
- ESTP - Entrepreneur
- ESFP - Entertainer