import { Link, useRouter } from "expo-router";
import { Text, View, TextInput, Button } from "react-native";

export default function Login() {
  const router = useRouter();

  return (
    <View>
      <Text className="text-white">INDEX</Text>
      <Button
        title="Login"
        onPress={() => {
          router.push("/login");
        }}
      />
      <Button
        title="Register"
        onPress={() => {
          router.push("/register");
        }}
      />

      <Button
        title="Tabs"
        onPress={() => {
          router.push("/(tabs)");
        }}
      />
      <Link href="/tinder" className="text-white">
        Tinder
      </Link>
    </View>
  );
}
