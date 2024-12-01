import { useLocalSearchParams } from "expo-router";
import { View, Text } from "react-native";

export default function HobbyDetails() {
  const { hobbyId } = useLocalSearchParams();

  return (
    <View>
      <Text>Details {hobbyId}</Text>
    </View>
  );
}
