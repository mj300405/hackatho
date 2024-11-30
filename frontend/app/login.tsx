import { View, Text, Button } from "react-native";
import Input from "@/components/forms/Input";
import { useState } from "react";
import axios, { AxiosError, AxiosResponse } from "axios";

export default function Register() {
  const [username, setUserName] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const [error, setError] = useState("");

  const handleLogin = () => {
    const requestBody = {
      username,
      password,
    };

    axios
      .post(`${process.env.EXPO_PUBLIC_SERVER_URL}/api/token/`, requestBody)
      .then((response: AxiosResponse) => {})
      .catch((e) => {
        if (e instanceof AxiosError) {
          setError(e.response?.data);
        }
      });
  };

  return (
    <View className="bg-white px-2 h-full">
      <Text className="text-center">LOGIN</Text>
      {error !== "" && <Text className="text-center text-red-400">LOGIN</Text>}
      <Input label="Login" value={username} onChangeText={setUserName} />
      <Input label="Password" value={password} onChangeText={setPassword} />
      <View className="h-10" /> {/* Spacer */}
      <Button title="Login" onPress={handleLogin} />
    </View>
  );
}
