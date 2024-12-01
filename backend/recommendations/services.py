import json
import openai
from django.conf import settings
from typing import List, Dict

class HobbyRecommendationService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def _create_prompt(self, user) -> str:
        # Get personality details if they exist
        personality_details = user.personality_details if user.personality_details else {}
        
        return f"""Based on the following detailed user profile, suggest 10 hobbies (6 best matches, 2 medium matches, 2 challenging matches).
        
        User Profile:
        Required Information:
        - Age: {user.age}
        - Location: {user.location}
        - Personality Type: {user.personality_type}
        - Available Time: {user.available_time} minutes per day
        - Budget Preference: {user.budget_preference}
        - Current Experience Points: {user.exp}
        
        Additional Information:
        - Personality Details: {json.dumps(personality_details, indent=2)}
        - Account Creation Date: {user.created_at.strftime('%Y-%m-%d')}
        
        Please consider all these factors, especially:
        - Location-specific opportunities and limitations
        - Age-appropriate activities
        - Time commitments that fit within their daily available time
        - Activities within their budget preference
        - Hobbies that match their personality type characteristics
        - Their current experience level (based on exp points)
        - Any specific traits or preferences from their personality details
        
        Respond with a JSON object containing a 'recommendations' array. Each hobby in the array should have:
        - name: The hobby name
        - description: A detailed description that explains why it matches their profile
        - difficulty_level: One of [BEGINNER, INTERMEDIATE, ADVANCED]
        - time_commitment: Required minutes per day
        - price_range: Estimated cost range (format: "$X-$Y")
        - required_equipment: List of essential items
        - minimum_age: Minimum recommended age
        - category_name: General category of the hobby
        - match_level: One of [BEST, MEDIUM, CHALLENGING]
        - location_suitable: Boolean indicating if the hobby is suitable for their location
        - personality_match: Brief explanation of why it matches their personality type

        The response should be in this format:
        {
            "recommendations": [
                {
                    "name": "Hobby Name",
                    "description": "Description with personalized reasoning",
                    ...
                }
            ]
        }"""

    def get_recommendations(self, user) -> List[Dict]:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                response_format={ "type": "json_object" },
                messages=[{
                    "role": "system",
                    "content": "You are a hobby recommendation assistant. Always respond with proper JSON format."
                }, {
                    "role": "user",
                    "content": self._create_prompt(user)
                }],
                temperature=0.7
            )
            
            recommendations = json.loads(response.choices[0].message.content)
            
            if isinstance(recommendations, dict) and 'recommendations' in recommendations:
                return recommendations['recommendations']
            
            return []
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []
