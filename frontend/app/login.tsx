import { View, Text, Button, TouchableOpacity } from "react-native";
import Input from "@/components/forms/Input";
import { useState, useContext } from "react";
import { axiosContext, AxiosContextType } from "@/lib/axios";
import axios, { AxiosError, AxiosResponse } from "axios";
import { useRouter } from "expo-router";
import { router } from "expo-router";

export default function Register() {
  const router = useRouter();
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

  //   return (
  //     <View className="bg-white px-2 h-full">
  //       <Text className="text-center">LOGIN</Text>
  //       {error !== "" && (
  //         <Text className="text-center text-red-400">{error}</Text>
  //       )}
  //       <Input label="Login" value={username} onChangeText={setUserName} />
  //       <Input label="Password" value={password} onChangeText={setPassword} />
  //       <View className="h-10" />
  //       <Button title="Login" onPress={handleLogin} />
  //     </View>
  //   );
  // }
  return (
    <View className="flex-1 bg-white px-8">
      <View className="flex-1 justify-end pb-12">
        {/* Header */}
        <View className="items-center mb-2">
          <Text className="text-2xl font-bold text-[#1A1C1E]">
            Welcome Back!
          </Text>
          <Text className="text-gray-500 mt-2">Please sign in to continue</Text>
        </View>

        {/* Error message */}
        {error !== "" && (
          <Text className="text-center text-red-500 mb-4">{error}</Text>
        )}

        {/* Form */}
        <View className="space-y-8">
          <Input
            placeholder="Username"
            placeholderTextColor="#9CA3AF"
            value={username}
            onChangeText={setUserName}
            className="bg-[#F5F6FA] rounded-xl p-4 mb-4"
          />
          <Input
            placeholder="Password"
            placeholderTextColor="#9CA3AF"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            className="bg-[#F5F6FA] rounded-xl p-4"
          />
        </View>

        {/* Login Button */}
        <TouchableOpacity
          className="bg-[#1A434F] rounded-xl py-4 mt-8"
          onPress={handleLogin}
        >
          <Text className="text-white text-center text-lg font-semibold">
            Sign In
          </Text>
        </TouchableOpacity>

        {/* Optional: Forgot Password */}
        <TouchableOpacity
          className="mt-4"
          onPress={() => router.push("/register")}
        >
          <Text className="text-[#1A434F] text-center">
            Don't have account? Register here
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
