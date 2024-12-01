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

export type Hobby = {
  id: number;
  name: string;
  description: string;
};
