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
    "name": "Urban Sketching",
    "description": "A creative hobby involving drawing city scenes...",
    "category": {
        "id": 1,
        "name": "Arts",
        "description": "Creative activities and artistic pursuits"
    },
    "difficulty_level": "BEGINNER",
    "time_commitment": 30,
    "price_range": "$20-$50",
    "required_equipment": ["sketchbook", "pencils", "pens"],
    "minimum_age": 12,
    "notes": "",
    "tags": [
        {
            "id": 1,
            "name": "creative"
        },
        {
            "id": 2,
            "name": "outdoor"
        }
    ],
    "user_status": "active",
    "user_notes": "Really enjoying this!",
    "user_rating": 5,
    "created_at": "2024-11-30T16:36:07Z"
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

### Bulk Update Hobby Status

**Endpoint:** `PATCH /api/hobbies/status/`

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Request Body:**
```json
[
    {
        "hobby_id": 1,
        "status": "favorite"
    },
    {
        "hobby_id": 2,
        "status": "completed"
    },
    {
        "hobby_id": 3,
        "status": "active"
    }
]
```

**Success Response (200 OK):**
```json
{
    "updated": [
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
            "rating": null
        }
    ],
    "errors": null
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

### Hobby Roulette

**Endpoint:** `POST /api/recommendations/roulette/`

**Description:** Generates a completely random hobby suggestion. Uses the roulette system which may require coins for non-free spins.

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Success Response (200 OK):**
```json
{
    "message": "Random hobby generated successfully",
    "history": {
        "id": 1,
        "hobby": {
            "id": 123,
            "name": "String",
            "description": "String",
            "difficulty_level": "BEGINNER|INTERMEDIATE|ADVANCED",
            "time_commitment": 30,
            "price_range": "$0-$50",
            "required_equipment": ["item1", "item2"],
            "minimum_age": 13,
            "category_name": "String"
        },
        "suggested_at": "2024-12-01T12:00:00Z",
        "was_accepted": false,
        "coins_spent": 50
    },
    "coins_spent": 50,
    "remaining_coins": 450
}
```

## Models

### Hobby
- `id`: Integer
- `name`: String
- `description`: Text
- `category`: ForeignKey to Category
- `difficulty_level`: String (BEGINNER, INTERMEDIATE, ADVANCED)
- `time_commitment`: Integer (minutes per day)
- `price_range`: String
- `required_equipment`: JSONField (list)
- `minimum_age`: Integer
- `notes`: Text
- `tags`: ManyToMany to Tag
- `created_at`: DateTime

### UserHobby
- `id`: Integer
- `user`: ForeignKey to User
- `hobby`: ForeignKey to Hobby
- `status`: String (active, favorite, completed)
- `notes`: Text
- `resources_links`: JSONField (list)
- `started_at`: DateTime
- `last_activity`: DateTime
- `rating`: Integer (1-5)

### Category
- `id`: Integer
- `name`: String
- `description`: Text

### Tag
- `id`: Integer
- `name`: String

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