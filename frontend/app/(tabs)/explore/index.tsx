import { ScrollView, Text } from "react-native";
import HobbyCard from "@/components/ui/HobbyCard";
import { GestureHandlerRootView } from "react-native-gesture-handler";

export default function Explore() {
  const hobbies = [
    {
      name: `Hiking`,
      description: "Desc.",
    },
    {
      name: `Biking`,
      description: "Desc.",
    },
    {
      name: `Swimming`,
      description: "Desc.",
    },
  ];

  return (
    <GestureHandlerRootView>
      <Text className="mt-5 m-3 text-3xl font-black">Explore new hobbies!</Text>
      <ScrollView
        contentContainerStyle={{
          display: "flex",
          alignItems: "center",
        }}
      >
        {hobbies.map((hobby, i) => (
          <HobbyCard key={i} hobby={hobby} />
        ))}
      </ScrollView>
    </GestureHandlerRootView>
  );
}
