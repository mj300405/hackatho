import Input from "@/components/forms/Input";
import {
  View,
  Text,
  Button,
  TouchableOpacity,
  SafeAreaView,
  Image,
  ScrollView,
  TextInput,
  TextInputProps,
} from "react-native";
import { useRef, useState } from "react";
import { Picker } from "@react-native-picker/picker";
import InputLabel from "@/components/forms/InputLabel";
import axios, { AxiosError } from "axios";
import { useRouter } from "expo-router";
import { router } from "expo-router";

export default function Register() {
  // Use state to store the values of the input fields
  const router = useRouter();
  const [username, setUserName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [repeatPassword, setRepeatPassword] = useState<string>("");
  const [age, setAge] = useState<string>("");
  const [location, setLocation] = useState<string>("");
  const [personality, setPersonality] = useState<string>("INTJ");
  const [availableTime, setAvailableTime] = useState<string>("");
  const [budget, setBudget] = useState<string>("LOW");

  const [error, setError] = useState<string>("");

  const ref = useRef<ScrollView | null>(null);

  const scrollToTop = () => {
    ref.current?.scrollTo({ y: 0, animated: true });
  };

  const handleRegister = () => {
    console.log("Registering user");
    if (password !== repeatPassword) {
      setError("Passwords do not match.");
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
      budget_preference: budget,
    };

    console.log(requestBody);

    axios
      .post(
        `http://${process.env.EXPO_PUBLIC_SERVER_URL}/api/auth/register/`,
        requestBody,
      )
      .then((response) => {
        console.log(response);
        router.navigate("/login");
      })
      .catch((error) => {
        // The response has validation errors.One key represents one form field. Each field has an array of errors.
        const keys = [
          "username",
          "email",
          "password",
          "age",
          "location",
          "personality_type",
          "available_time",
          "budget_preferences",
        ];

        if (error instanceof AxiosError) {
          console.error(error.response?.data);
          keys.forEach((key) => {
            if (error.response?.data[key]) {
              setError(`${key}: ${error.response?.data[key][0]}`);
              scrollToTop();
            }
          });
        }
      });
  };

  return (
    <SafeAreaView className="flex-1 bg-white">
      <ScrollView showsVerticalScrollIndicator={false} ref={ref}>
        <View className="px-8">
          {/* Header */}
          <View className="items-center mt-12 mb-8">
            <Text className="text-2xl font-bold text-[#1A1C1E]">
              Create Account
            </Text>
            <Text className="text-gray-500 mt-2">
              Please fill in the details
            </Text>
          </View>

          {/* Error message */}
          {error !== "" && (
            <Text className="text-center text-red-500 mb-4">{error}</Text>
          )}

          {/* Form Fields */}
          <Input
            placeholder="Username"
            placeholderTextColor="#9CA3AF"
            onChangeText={setUserName}
            value={username}
            className="bg-[#F5F6FA] rounded-xl p-4 mb-4"
          />

          <Input
            placeholder="Email"
            placeholderTextColor="#9CA3AF"
            onChangeText={setEmail}
            value={email}
            className="bg-[#F5F6FA] rounded-xl p-4 mb-4"
          />

          <Input
            placeholder="Password"
            placeholderTextColor="#9CA3AF"
            onChangeText={setPassword}
            value={password}
            secureTextEntry={true}
            className="bg-[#F5F6FA] rounded-xl p-4 mb-4"
          />

          <Input
            placeholder="Repeat Password"
            placeholderTextColor="#9CA3AF"
            onChangeText={setRepeatPassword}
            value={repeatPassword}
            secureTextEntry={true}
            className="bg-[#F5F6FA] rounded-xl p-4 mb-4"
          />

          <Input
            placeholder="Age"
            placeholderTextColor="#9CA3AF"
            onChangeText={setAge}
            value={age}
            keyboardType="numeric"
            className="bg-[#F5F6FA] rounded-xl p-4 mb-4"
          />

          <Input
            placeholder="Location"
            placeholderTextColor="#9CA3AF"
            onChangeText={setLocation}
            value={location}
            className="bg-[#F5F6FA] rounded-xl p-4 mb-4"
          />

          <Input
            placeholder="Available Time"
            placeholderTextColor="#9CA3AF"
            onChangeText={setAvailableTime}
            value={availableTime}
            className="bg-[#F5F6FA] rounded-xl p-4 mb-4"
          />

          <View className="bg-[#F5F6FA] rounded-xl mb-4">
            <Picker selectedValue={personality} onValueChange={setPersonality}>
              <Picker.Item
                label="Architect (INTJ)"
                value="INTJ"
                color="#9CA3AF"
              />
              <Picker.Item
                label="Logician (INTP)"
                value="INTP"
                color="#9CA3AF"
              />
              <Picker.Item
                label="Commander (ENTJ)"
                value="ENTJ"
                color="#9CA3AF"
              />
              <Picker.Item
                label="Debater (ENTP)"
                value="ENTP"
                color="#9CA3AF"
              />
              <Picker.Item
                label="Advocate (INFJ)"
                value="INFJ"
                color="#9CA3AF"
              />
              <Picker.Item
                label="Mediator (INFP)"
                value="INFP"
                color="#9CA3AF"
              />
              <Picker.Item
                label="Protagonist (ENFJ)"
                value="ENFJ"
                color="#9CA3AF"
              />
              <Picker.Item
                label="Campaigner (ENFP)"
                value="ENFP"
                color="#9CA3AF"
              />
              <Picker.Item
                label="Logistician (ISTJ)"
                value="ISTJ"
                color="#9CA3AF"
              />
              <Picker.Item
                label="Defender (ISFJ)"
                value="ISFJ"
                color="#9CA3AF"
              />
              <Picker.Item
                label="Executive (ESTJ)"
                value="ESTJ"
                color="#9CA3AF"
              />
              <Picker.Item label="Consul (ESFJ)" value="ESFJ" color="#9CA3AF" />
              <Picker.Item
                label="Virtuoso (ISTP)"
                value="ISTP"
                color="#9CA3AF"
              />
              <Picker.Item
                label="Adventurer (ISFP)"
                value="ISFP"
                color="#9CA3AF"
              />
              <Picker.Item
                label="Entrepreneur (ESTP)"
                value="ESTP"
                color="#9CA3AF"
              />
              <Picker.Item
                label="Entertainer (ESFP)"
                value="ESFP"
                color="#9CA3AF"
              />
            </Picker>
          </View>

          <View className="bg-[#F5F6FA] rounded-xl mb-4">
            <Picker selectedValue={budget} onValueChange={setBudget}>
              <Picker.Item label="Low Budget" value="LOW" color="#9CA3AF" />
              <Picker.Item
                label="Medium Budget"
                value="MEDIUM"
                color="#9CA3AF"
              />
              <Picker.Item label="High Budget" value="HIGH" color="#9CA3AF" />
            </Picker>
          </View>

          {/* Buttons */}
          <TouchableOpacity
            className="bg-[#1A434F] rounded-xl py-4 mt-8 mb-4"
            onPress={handleRegister}
          >
            <Text className="text-white text-center text-lg font-semibold">
              Create Account
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            className="mb-12"
            onPress={() => router.push("/login")}
          >
            <Text className="text-[#1A434F] text-center">
              Already have an account? Sign in
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
