# Hobby Discovery API Documentation

## Table of Contents
- [Authentication](#authentication)
  - [Registration](#registration)
  - [Login](#login)
  - [Token Refresh](#token-refresh)
  - [User Details](#user-details)
- [Hobbies](#hobbies)
  - [List All User Hobbies](#list-all-user-hobbies)
  - [List User Hobbies By Status](#list-user-hobbies-by-status)
  - [Get Hobby Details](#get-hobby-details)
  - [Update Hobby Status](#update-hobby-status)
  - [Bulk Update Hobby Status](#bulk-update-hobby-status)
- [Recommendations](#recommendations)
  - [Initial Recommendations](#initial-recommendations)
  - [Hobby Roulette](#hobby-roulette)
- [Models](#models)
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

### List All User Hobbies

**Endpoint:** `GET /api/hobbies/user/hobbies/`

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Query Parameters:**
- `status`: Filter by status (active/favorite/completed)
- `search`: Search hobbies by name or description
- `sort`: Sort by field (name, started_at, last_activity)

**Success Response (200 OK):**
```json
{
    "total_count": 3,
    "hobbies": {
        "active": [
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
                "started_at": "2024-11-30T16:36:07Z",
                "last_activity": "2024-11-30T16:36:07Z",
                "rating": 5,
                "days_active": 1
            }
        ],
        "favorite": [],
        "completed": []
    }
}
```

### List User Hobbies By Status

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

[Rest of documentation continues as before...]

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

### Hobby List Endpoints
- `/api/hobbies/user/hobbies/`: New endpoint with filtering, sorting, and grouping
- `/api/hobbies/my/`: Legacy endpoint for basic hobby listing

### Status Update Methods
- Single hobby update: Use when updating one hobby at a time with detailed information (notes, rating)
- Bulk update: Use when changing status for multiple hobbies simultaneously
- Both methods support the same status types: active, favorite, completed

### Roulette System
- One free spin every 24 hours
- Non-free spins cost coins (amount based on system settings)
- Profile must be complete to use this feature
- Generated hobby is automatically saved to user's history
- The `was_accepted` field starts as `false` and can be updated later

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