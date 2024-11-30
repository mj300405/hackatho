import Input from "@/components/forms/Input";
import { View, Text } from "react-native";
import { useState } from "react";
import { Picker } from "@react-native-picker/picker";
import InputLabel from "@/components/forms/InputLabel";

export default function Register() {
  const [username, setUserName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [age, setAge] = useState<string>("");
  const [location, setLocation] = useState<string>(""); // Napis miejscowości
  const [personality, setPersonality] = useState<string>(""); // Napis miejscowości
  const [availableTime, setAvailableTime] = useState<string>(""); // Napis miejscowości
  const [budget, setBudget] = useState<string>(""); // Napis miejscowości

  return (
    <View className="bg-white">
			<Text className="text-center">Register</Text>
      <Input label="Username" onChangeText={setUserName} value={username} />
      <Input label="Email" onChangeText={setEmail} value={email} />
      <Input
        label="Password"
        onChangeText={setPassword}
        value={password}
        secureTextEntry={true}
      />
      <Input
        label="Age"
        onChangeText={setAge}
        value={age}
        keyboardType="numeric"
      />
      <Input label="Location" onChangeText={setLocation} value={location} />
      <Input
        label="Available Time"
        onChangeText={setAvailableTime}
        value={availableTime}
      />

      <InputLabel>Personality Type</InputLabel>
      <Picker selectedValue={personality} onValueChange={setPersonality}>
        <Picker.Item label="Architect (INTJ)" value="INTJ" />
        <Picker.Item label="Logician (INTP)" value="INTP" />
        <Picker.Item label="Commander (ENTJ)" value="ENTJ" />
        <Picker.Item label="Debater (ENTP)" value="ENTP" />
        <Picker.Item label="Advocate (INFJ)" value="INFJ" />
        <Picker.Item label="Mediator (INFP)" value="INFP" />
        <Picker.Item label="Protagonist (ENFJ)" value="ENFJ" />
        <Picker.Item label="Campaigner (ENFP)" value="ENFP" />
        <Picker.Item label="Logistician (ISTJ)" value="ISTJ" />
        <Picker.Item label="Defender (ISFJ)" value="ISFJ" />
        <Picker.Item label="Executive (ESTJ)" value="ESTJ" />
        <Picker.Item label="Consul (ESFJ)" value="ESFJ" />
        <Picker.Item label="Virtuoso (ISTP)" value="ISTP" />
        <Picker.Item label="Adventurer (ISFP)" value="ISFP" />
        <Picker.Item label="Entrepreneur (ESTP)" value="ESTP" />
        <Picker.Item label="Entertainer (ESFP)" value="ESFP" />
      </Picker>
      <InputLabel>Budget</InputLabel>
      <Picker selectedValue={budget} onValueChange={setBudget}>
        <Picker.Item label="LOW" value="LOW" />
        <Picker.Item label="MEDIUM" value="MEDIUM" />
        <Picker.Item label="HIGH" value="HIGH" />
      </Picker>
    </View>
  );
}

// {
//     "username": "testuser",
//     "email": "test@example.com",
//     "password": "yourpassword123",
//     "age": 25,
//     "location": "Warsaw",
//     "personality_type": "INTJ",
//     "available_time": 60,
//     "budget_preference": "MEDIUM" LOW MEDIUM
// }
