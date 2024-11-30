import json
import openai
from django.conf import settings
from typing import List, Dict

class HobbyRecommendationService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def _create_prompt(self, user) -> str:
        return f"""Based on the following user profile, suggest 10 hobbies (6 best matches, 2 medium matches, 2 challenging matches).
        User Profile:
        - Personality: {user.personality_type}
        - Available time: {user.available_time} minutes per day
        - Budget: {user.budget_preference}
        - Age: {user.age}

        Respond with a JSON object containing a 'recommendations' array. Each hobby in the array should have:
        - name: The hobby name
        - description: A detailed description
        - difficulty_level: One of [BEGINNER, INTERMEDIATE, ADVANCED]
        - time_commitment: Required minutes per day
        - price_range: Estimated cost range (format: "$X-$Y")
        - required_equipment: List of essential items
        - minimum_age: Minimum recommended age
        - category_name: General category of the hobby
        - match_level: One of [BEST, MEDIUM, CHALLENGING]

        The response should be in this format:
        {
            "recommendations": [
                {
                    "name": "Hobby Name",
                    "description": "Description",
                    ...
                }
            ]
        }"""

    def get_recommendations(self, user) -> List[Dict]:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
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
