export type User = {
  id: number;
  username: string;
  email: string;
  age: number;
  location: string;
  personality_type: string;
  available_time: number;
  budget_preference: string;
  profile_completed: boolean;
  coins: number;
  exp: number;
};

export type HobbyRouletteResponse = {
  coins_spent: number;
  history: {
    coins_spent: number;
    hobby: HobbyType;
    id: number;
    suggested_at: string;
    was_accepted: boolean;
  };
  message: string;
  recommendation: HobbyType;
  remaining_coins: number;
};

export type Direction = "left" | "right" | "up" | "down";

export type HobbyType = {
  id: number;
  name: string;
  description: string;
  difficulty_level: string;
  time_commitment: number;
  price_range: string;
  required_equipment: string[];
  minimum_age: number;
  match_level: string;
};

export type UserHobby = {
  days_active: number;
  hobby: {
    category: {
      description: string;
      id: number;
      name: string;
    };
    description: string;
    difficulty_level: string;
    id: number;
    minimum_age: number;
    name: string;
    price_range: string;
    required_equipment: string[];
    time_commitment: number;
  };
  id: number;
  last_activity: string;
  notes: string;
  rating: null;
  started_at: string;
  status: string;
};
