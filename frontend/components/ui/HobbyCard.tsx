import { View, Text } from "react-native";
import { Gesture, GestureDetector } from "react-native-gesture-handler";
import { LinearGradient } from "expo-linear-gradient";

import type { HobbyType } from "@/lib/types";
import { router } from "expo-router";

export default function HobbyCard({ hobby }: { hobby: HobbyType }) {
  console.log(hobby);
  const tap = Gesture.Tap()
    .numberOfTaps(1)
    .maxDuration(250)
    .runOnJS(true)
    .onEnd(() => {
      // TODO: Navigate to the details screen
      router.push(`/(tabs)/details/${hobby.id}`);
    });

  return (
    <GestureDetector gesture={tap}>
      <LinearGradient
        colors={["#C3F44D", "#FAF3EB"]}
        className="flex overflow-hidden rounded-2xl w-[90%] mx-[5%] my-2 mb-4"
        style={{}}
      >
        <View className="h-20 rounded-xl" />
        <View className="p-2 bg-[#D3C2F8] rounded-lg">
          <Text className="font-bold">{hobby.name}</Text>
          <Text>{hobby.description}</Text>
        </View>
      </LinearGradient>
    </GestureDetector>
  );
}
