import { useRouter, Link } from "expo-router";
import {
  Text,
  View,
  TextInput,
  Button,
  Image,
  TouchableOpacity,
} from "react-native";

export default function Login() {
  const router = useRouter();

  return (
    <View className="flex-1 bg-white px-8">
      {/* Header container - now centered */}
      <View className="flex-1 justify-center items-center">
        <View className="flex-row items-center">
          <Image
            source={require("@/assets/images/app-icon.png")}
            style={{ width: 32, height: 32 }}
            className="mr-3"
          />
          <Text className="text-2xl font-bold text-[#1A1C1E]">Hobbyverse</Text>
        </View>

        {/* Image placeholder */}
        <Image
          source={require("@/assets/images/index-photo.png")}
          style={{ width: 400, height: 400, resizeMode: "contain" }}
          className="p-3"
        />

        {/* Text content */}
        <View className="px-4 mt-8">
          <Text className="text-3xl font-bold text-center text-[#1A1C1E]">
            Explore new hobbies and compete with others
          </Text>
        </View>
      </View>

      {/* Buttons */}
      <View className="mb-12">
        <TouchableOpacity
          className="bg-[#1A434F] rounded-xl py-4 mb-4"
          onPress={() => router.push("/login")}
        >
          <Text className="text-white text-center text-lg font-semibold">
            Sign In
          </Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => router.push("/register")}>
          <Text className="text-[#1A1C1E] text-center text-lg font-semibold">
            Sign Up
          </Text>
        </TouchableOpacity>

        {/* to usunąć */}
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
    </View>
  );
}
