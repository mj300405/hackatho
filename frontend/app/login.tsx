import { View, Text } from "react-native";
import Input from "@/components/forms/Input";
import { useState } from "react";

export default function Register() {
  const [userName, setUserName] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  return (
    <View className="bg-white">
      <Text className="text-center">LOGIN</Text>
      <Input label="Login" value={userName} onChangeText={setUserName} />
      <Input label="Password" value={password} onChangeText={setPassword} />
    </View>
  );
}
