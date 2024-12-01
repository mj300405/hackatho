from typing import List, Dict
import json
import openai
from django.conf import settings

class HobbyRecommendationService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    def _create_system_prompt(self) -> str:
        return """You are a hobby recommendation assistant. For each user, provide personalized hobby suggestions based on their profile, considering:
        - How the hobby matches their personality type
        - Whether it fits within their available time
        - If it's appropriate for their location
        - If it matches their budget constraints
        - Age appropriateness
        
        Always ensure recommendations are safe, ethical, and well-suited to the user's constraints."""

    def _create_user_prompt(self, user) -> str:
        personality_details = user.personality_details if user.personality_details else {}
        
        return f"""Please recommend 10 hobbies based on this user profile:

        PROFILE:
        - Age: {user.age}
        - Location: {user.location}
        - MBTI Type: {user.personality_type}
        - Daily Available Time: {user.available_time} minutes
        - Budget Level: {user.budget_preference}
        - Experience Points: {user.exp}
        - Personality Details: {json.dumps(personality_details, indent=2)}

        FORMAT REQUIREMENTS:
        Return exactly 10 hobbies in this JSON structure:
        {{
            "recommendations": [
                {{
                    "name": "string",
                    "description": "string",
                    "difficulty_level": "BEGINNER|INTERMEDIATE|ADVANCED",
                    "time_commitment": integer (minutes per day),
                    "price_range": "string ($X-$Y format)",
                    "required_equipment": ["item1", "item2"],
                    "minimum_age": integer,
                    "category_name": "string",
                    "match_level": "BEST|MEDIUM|CHALLENGING"
                }}
            ]
        }}

        DISTRIBUTION:
        - 6 BEST matches (highly aligned with profile)
        - 2 MEDIUM matches (moderate alignment)
        - 2 CHALLENGING matches (stretch goals)"""

    def get_recommendations(self, user) -> List[Dict]:
        try:
            print(f"Generating recommendations for user {user.id}")
            
            response = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "system",
                        "content": self._create_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": self._create_user_prompt(user)
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            # Extract the content from the response
            content = response.choices[0].message.content
            recommendations = json.loads(content)

            # Validate the response structure
            if not isinstance(recommendations, dict) or 'recommendations' not in recommendations:
                raise ValueError("Invalid response format from OpenAI API")

            # Validate each recommendation
            for rec in recommendations['recommendations']:
                required_fields = ['name', 'description', 'difficulty_level', 'time_commitment', 
                                 'price_range', 'required_equipment', 'minimum_age', 
                                 'category_name', 'match_level']
                
                missing_fields = [field for field in required_fields if field not in rec]
                if missing_fields:
                    raise ValueError(f"Missing required fields in recommendation: {missing_fields}")

                # Validate specific field values
                if rec['difficulty_level'] not in ['BEGINNER', 'INTERMEDIATE', 'ADVANCED']:
                    raise ValueError(f"Invalid difficulty_level for hobby {rec['name']}")
                
                if rec['match_level'] not in ['BEST', 'MEDIUM', 'CHALLENGING']:
                    raise ValueError(f"Invalid match_level for hobby {rec['name']}")

            print(f"Successfully generated {len(recommendations['recommendations'])} recommendations")
            return recommendations['recommendations']

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            raise Exception("Failed to parse API response")
        except openai.APIError as e:
            print(f"OpenAI API error: {str(e)}")
            raise Exception(f"OpenAI API error: {str(e)}")
        except ValueError as e:
            print(f"Validation error: {str(e)}")
            raise Exception(f"Invalid recommendation format: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise Exception(f"Failed to generate recommendations: {str(e)}")

class ExplorationRecommendationService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    def _create_system_prompt(self) -> str:
        return """You are a hobby exploration assistant. Your role is to suggest new hobbies that complement and build upon a user's existing interests and activities.
        Consider:
        - How new hobbies can complement existing ones
        - Skills that transfer between hobbies
        - Total time commitment across all hobbies
        - Overall budget impact
        - Progressive skill development"""

    def _format_hobby_info(self, hobby):
        return {
            "name": hobby.hobby.name,
            "category": hobby.hobby.category.name if hobby.hobby.category else "Unknown",
            "difficulty_level": hobby.hobby.difficulty_level,
            "time_commitment": hobby.hobby.time_commitment
        }

    def _create_user_prompt(self, user, active_hobbies, favorite_hobbies) -> str:
        active_hobbies_info = [self._format_hobby_info(h) for h in active_hobbies]
        favorite_hobbies_info = [self._format_hobby_info(h) for h in favorite_hobbies]
        
        total_active_time = sum(h.hobby.time_commitment for h in active_hobbies)
        
        return f"""Based on this user's profile and current hobbies, suggest 5 NEW hobbies they might enjoy.

        USER PROFILE:
        - Age: {user.age}
        - Location: {user.location}
        - MBTI Type: {user.personality_type}
        - Daily Available Time: {user.available_time} minutes
        - Currently Used Time: {total_active_time} minutes
        - Remaining Free Time: {max(0, user.available_time - total_active_time)} minutes
        - Budget Level: {user.budget_preference}
        
        CURRENT ACTIVE HOBBIES:
        {json.dumps(active_hobbies_info, indent=2)}
        
        FAVORITE HOBBIES:
        {json.dumps(favorite_hobbies_info, indent=2)}

        REQUIREMENTS:
        1. Suggest exactly 5 new hobbies not in their current lists
        2. Each hobby should complement existing ones
        3. Consider remaining free time in suggestions
        4. Stay within remaining budget capacity
        5. Progress logically from current skill levels

        FORMAT REQUIREMENTS:
        Return exactly 5 hobbies in this JSON structure:
        {{
            "recommendations": [
                {{
                    "name": "string",
                    "description": "string",
                    "difficulty_level": "BEGINNER|INTERMEDIATE|ADVANCED",
                    "time_commitment": integer (minutes per day),
                    "price_range": "string ($X-$Y format)",
                    "required_equipment": ["item1", "item2"],
                    "minimum_age": integer,
                    "category_name": "string",
                    "match_level": "BEST|MEDIUM|CHALLENGING"
                }}
            ]
        }}"""

    def get_recommendations(self, user, active_hobbies, favorite_hobbies) -> List[Dict]:
        try:
            print(f"Generating exploration recommendations for user {user.id}")
            
            response = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "system",
                        "content": self._create_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": self._create_user_prompt(user, active_hobbies, favorite_hobbies)
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            content = response.choices[0].message.content
            recommendations = json.loads(content)

            if not isinstance(recommendations, dict) or 'recommendations' not in recommendations:
                raise ValueError("Invalid response format from OpenAI API")

            # Validate recommendations
            for rec in recommendations['recommendations']:
                required_fields = ['name', 'description', 'difficulty_level', 'time_commitment', 
                                 'price_range', 'required_equipment', 'minimum_age', 
                                 'category_name', 'match_level']
                
                missing_fields = [field for field in required_fields if field not in rec]
                if missing_fields:
                    raise ValueError(f"Missing required fields in recommendation: {missing_fields}")

                if rec['difficulty_level'] not in ['BEGINNER', 'INTERMEDIATE', 'ADVANCED']:
                    raise ValueError(f"Invalid difficulty_level for hobby {rec['name']}")
                
                if rec['match_level'] not in ['BEST', 'MEDIUM', 'CHALLENGING']:
                    raise ValueError(f"Invalid match_level for hobby {rec['name']}")

                # Additional validation for exploration recommendations
                if any(rec['name'].lower() == h.hobby.name.lower() for h in active_hobbies):
                    raise ValueError(f"Recommendation {rec['name']} is already an active hobby")
                
                if any(rec['name'].lower() == h.hobby.name.lower() for h in favorite_hobbies):
                    raise ValueError(f"Recommendation {rec['name']} is already a favorite hobby")

            print(f"Successfully generated {len(recommendations['recommendations'])} exploration recommendations")
            return recommendations['recommendations']

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            raise Exception("Failed to parse API response")
        except openai.APIError as e:
            print(f"OpenAI API error: {str(e)}")
            raise Exception(f"OpenAI API error: {str(e)}")
        except ValueError as e:
            print(f"Validation error: {str(e)}")
            raise Exception(f"Invalid recommendation format: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise Exception(f"Failed to generate recommendations: {str(e)}")