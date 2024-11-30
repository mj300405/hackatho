# Hobby Discovery API Documentation

## Table of Contents
- [Authentication](#authentication)
  - [Registration](#registration)
  - [Login](#login)
  - [Token Refresh](#token-refresh)
  - [User Details](#user-details)
- [Hobbies](#hobbies)
  - [List User Hobbies](#list-user-hobbies)
  - [Get Hobby Details](#get-hobby-details)
  - [Update Hobby Status](#update-hobby-status)
- [Recommendations](#recommendations)
  - [Initial Recommendations](#initial-recommendations)
- [Important Notes](#important-notes)

## Authentication

### Registration

**Endpoint:** `POST /api/auth/register/`

**Request Body:**
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

**Success Response (201 Created):**
```json
{
    "id": 1,
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
    "budget_preference": "MEDIUM",
    "profile_completed": false,
    "coins": 0,
    "exp": 0
}
```

### Login

**Endpoint:** `POST /api/auth/token/`

**Request Body:**
```json
{
    "username": "testuser",
    "password": "yourpassword123"
}
```

**Success Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Token Refresh

**Endpoint:** `POST /api/auth/token/refresh/`

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Success Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### User Details

**Endpoint:** `GET /api/auth/user/`

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Success Response (200 OK):**
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
    "profile_completed": true,
    "coins": 0,
    "exp": 0
}
```

## Hobbies

### List User Hobbies

**Endpoint:** `GET /api/hobbies/my/`

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Success Response (200 OK):**
```json
[
    {
        "id": 1,
        "hobby": {
            "id": 1,
            "name": "Urban Sketching",
            "description": "A creative hobby involving drawing city scenes...",
            "difficulty_level": "BEGINNER",
            "time_commitment": 30,
            "price_range": "$20-$50",
            "required_equipment": ["sketchbook", "pencils", "pens"],
            "minimum_age": 12
        },
        "status": "active",
        "notes": "Really enjoying this!",
        "resources_links": [],
        "started_at": "2024-11-30T16:36:07Z",
        "last_activity": "2024-11-30T16:36:07Z",
        "rating": 5
    }
]
```

### Get Hobby Details

**Endpoint:** `GET /api/hobbies/{hobby_id}/`

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Success Response (200 OK):**
```json
{
    "id": 1,
    "hobby": {
        "id": 1,
        "name": "Urban Sketching",
        "description": "A creative hobby involving drawing city scenes...",
        "difficulty_level": "BEGINNER",
        "time_commitment": 30,
        "price_range": "$20-$50",
        "required_equipment": ["sketchbook", "pencils", "pens"],
        "minimum_age": 12
    },
    "status": "active",
    "notes": "Really enjoying this!",
    "resources_links": [],
    "started_at": "2024-11-30T16:36:07Z",
    "last_activity": "2024-11-30T16:36:07Z",
    "rating": 5
}
```

### Update Hobby Status

**Endpoint:** `PATCH /api/hobbies/{hobby_id}/status/`

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Request Body:**
```json
{
    "status": "favorite",
    "notes": "Really enjoying this hobby!",
    "rating": 5
}
```

**Success Response (200 OK):**
```json
{
    "id": 1,
    "hobby": {
        "id": 1,
        "name": "Urban Sketching",
        "description": "A creative hobby involving drawing city scenes...",
        "difficulty_level": "BEGINNER",
        "time_commitment": 30,
        "price_range": "$20-$50",
        "required_equipment": ["sketchbook", "pencils", "pens"],
        "minimum_age": 12
    },
    "status": "favorite",
    "notes": "Really enjoying this hobby!",
    "resources_links": [],
    "started_at": "2024-11-30T16:36:07Z",
    "last_activity": "2024-11-30T16:36:07Z",
    "rating": 5
}
```

## Recommendations

### Initial Recommendations

**Endpoint:** `GET /api/recommendations/initial/{user_id}/`

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Success Response (200 OK):**
```json
{
    "message": "Initial recommendations generated successfully",
    "recommendations": [
        {
            "id": 1,
            "name": "Urban Sketching",
            "description": "A creative hobby involving drawing city scenes...",
            "difficulty_level": "BEGINNER",
            "time_commitment": 30,
            "price_range": "$20-$50",
            "required_equipment": ["sketchbook", "pencils", "pens"],
            "minimum_age": 12,
            "match_level": "BEST"
        }
    ]
}
```

## Important Notes

### Authentication
- Access token expires in 60 minutes
- Include access token in all authenticated requests
- Use refresh token to get new access token when needed

### Required Fields
**Registration:**
- username
- email
- password
- age
- location
- personality_type

### Optional Fields
**Registration:**
- personality_details
- available_time (defaults to 60)
- budget_preference (defaults to "MEDIUM")

### Status Types
- active: Currently pursuing
- favorite: Marked as favorite
- completed: Finished or mastered

### Error Responses

**401 Unauthorized:**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden:**
```json
{
    "error": "Profile incomplete",
    "message": "Please complete your profile before accessing this feature"
}
```

**404 Not Found:**
```json
{
    "error": "Hobby not found for this user"
}
```

**400 Bad Request:**
```json
{
    "error": "Invalid status",
    "message": "Status must be one of: active, favorite, completed"
}
```