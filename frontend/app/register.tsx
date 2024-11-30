import Input from "@/components/forms/Input";
import { View, Text, Button } from "react-native";
import { useState } from "react";
import { Picker } from "@react-native-picker/picker";
import InputLabel from "@/components/forms/InputLabel";
import axios from "axios";

export default function Register() {
  const [username, setUserName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [repeatPassword, setRepeatPassword] = useState<string>("");
  const [age, setAge] = useState<string>("");
  const [location, setLocation] = useState<string>(""); 
  const [personality, setPersonality] = useState<string>("INTJ"); 
  const [availableTime, setAvailableTime] = useState<string>(""); 
  const [budget, setBudget] = useState<string>("LOW"); 

	const handleRegister = async () => {
	console.log("Registering user");
		if (password !== repeatPassword) {
			console.log("Passwords do not match");
			// TODO: show error
			return;
		}

		const requestBody = {
			username,
			email,
			password,
			age,
			location,
			personality_type: personality,
			available_time: availableTime,
			budget_preference: budget
		};

		console.log(requestBody);
		const response = await axios.post("http://localhost:8000/api/register", requestBody);
		console.log(response);
	};

  return (
    <View className="bg-white px-2">
			<Text className="text-center">Register</Text>
      <Input label="Username" onChangeText={setUserName} value={username} placeholder="Username"/>
      <Input label="Email" onChangeText={setEmail} value={email} placeholder="Email"/>
      <Input
        label="Password"
        onChangeText={setPassword}
        value={password}
        secureTextEntry={true}
				placeholder="Password"
      />
			<Input
        label="Repeat Password"
        onChangeText={setRepeatPassword}
        value={repeatPassword}
        secureTextEntry={true}
				placeholder="Password"
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
			 <Button title="Register" onPress={handleRegister}/>
    </View>
  );
}
