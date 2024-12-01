from typing import Dict, List
import json
import openai
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from challenges.models import Challenge

class ChallengeGenerationService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    def _format_challenge_info(self, challenge: Challenge) -> Dict:
        return {
            "description": challenge.description,
            "target": challenge.target,
            "reward": challenge.reward,
            "created_at": challenge.created_at.isoformat(),
            "successful": challenge.successful
        }

    def _create_system_prompt(self) -> str:
        return """You are a challenge generation assistant. Your role is to create engaging, 
        achievable challenges for users based on their hobbies. Each challenge should:
        - Be specific and measurable
        - Have a clear target/goal
        - Be achievable within 1-7 days
        - Have an appropriate reward in coins (10-100)
        - Not repeat recent challenges
        - Match the hobby's difficulty level"""

    def _create_user_prompt(self, user, hobby, past_challenges: List[Challenge]) -> str:
        past_challenges_info = [self._format_challenge_info(c) for c in past_challenges]
        
        return f"""Generate a new challenge for this user and hobby:

        USER INFO:
        - Age: {user.age}
        - Available daily time: {user.available_time} minutes
        - Experience level: {user.exp} points
        
        HOBBY INFO:
        - Name: {hobby.name}
        - Difficulty: {hobby.difficulty_level}
        - Time commitment: {hobby.time_commitment} minutes per day
        
        PAST CHALLENGES:
        {json.dumps(past_challenges_info, indent=2)}

        REQUIREMENTS:
        Return a single challenge in this JSON format:
        {
            "description": "string (specific task description)",
            "target": integer (number of times to complete),
            "reward": integer (coins between 10-100),
            "duration_days": integer (1-7)
        }

        Examples:
        - For hiking: "Walk 5000 steps in nature" (target: 1)
        - For gym: "Complete a full workout session" (target: 5)
        - For reading: "Read for 30 minutes" (target: 7)
        
        Avoid generating challenges similar to the past challenges shown above."""

    def generate_challenge(self, user, hobby, past_challenges: List[Challenge] = None) -> Dict:
        if past_challenges is None:
            past_challenges = []

        try:
            print(f"Generating challenge for user {user.id} and hobby {hobby.name}")
            
            response = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "system",
                        "content": self._create_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": self._create_user_prompt(user, hobby, past_challenges)
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.8
            )

            content = response.choices[0].message.content
            challenge_data = json.loads(content)

            # Validate the challenge data
            required_fields = ['description', 'target', 'reward', 'duration_days']
            missing_fields = [field for field in required_fields if field not in challenge_data]
            if missing_fields:
                raise ValueError(f"Missing required fields in challenge: {missing_fields}")

            # Validate specific fields
            if not (10 <= challenge_data['reward'] <= 100):
                raise ValueError("Reward must be between 10 and 100 coins")
            
            if not (1 <= challenge_data['duration_days'] <= 7):
                raise ValueError("Duration must be between 1 and 7 days")

            if not (1 <= challenge_data['target'] <= 100):
                raise ValueError("Target must be between 1 and 100")

            # Calculate expiration date
            expiration_date = timezone.now() + timedelta(days=challenge_data['duration_days'])

            # Create challenge object (without saving)
            challenge = Challenge(
                hobby=hobby,
                user=user,
                description=challenge_data['description'],
                reward=challenge_data['reward'],
                target=challenge_data['target'],
                expiration_date=expiration_date
            )

            print(f"Successfully generated challenge: {challenge_data['description']}")
            return challenge

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            raise Exception("Failed to parse API response")
        except openai.APIError as e:
            print(f"OpenAI API error: {str(e)}")
            raise Exception(f"OpenAI API error: {str(e)}")
        except ValueError as e:
            print(f"Validation error: {str(e)}")
            raise Exception(f"Invalid challenge format: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise Exception(f"Failed to generate challenge: {str(e)}")