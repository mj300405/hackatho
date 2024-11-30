import { View, Text, Button } from "react-native";
import Input from "@/components/forms/Input";
import { useState, useContext } from "react";
import { axiosContext, AxiosContextType } from "@/lib/axios";
import axios, { AxiosError, AxiosResponse } from "axios";

export default function Register() {
  // Use state to store the values of the input fields
  const [username, setUserName] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  // Use state to store the error message
  const [error, setError] = useState("");

  // Context to set the tokens

  const authContext = useContext(axiosContext) as AxiosContextType;
  const handleLogin = () => {
    const requestBody = {
      username,
      password,
    };

    axios
      .post(
        `http://${process.env.EXPO_PUBLIC_SERVER_URL}/api/auth/token/`,
        requestBody,
      )
      .then((response: AxiosResponse) => {
        const { access, refresh } = response.data;
        authContext.setToken(access);
        authContext.setRefreshToken(refresh);
      })
      .catch((e) => {
        if (e instanceof AxiosError) {
          setError(e.response?.data);
          console.error(e.toJSON());
        }
      });
  };

  return (
    <View className="bg-white px-2 h-full">
      <Text className="text-center">LOGIN</Text>
      {error !== "" && (
        <Text className="text-center text-red-400">{error}</Text>
      )}
      <Input label="Login" value={username} onChangeText={setUserName} />
      <Input label="Password" value={password} onChangeText={setPassword} />
      <View className="h-10" />
      <Button title="Login" onPress={handleLogin} />
    </View>
  );
}
