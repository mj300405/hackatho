import { ThemedText } from "@/components/ThemedText";
//import { Text, View } from "react-native";

// export default function Profile() {
//   return (
//     <View>
//       <ThemedText>Profile</ThemedText>
//     </View>
//   );
// }
import { View, Text, Image, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { IconSymbol } from "@/components/ui/IconSymbol";
import { Colors } from "@/constants/Colors";
import { useColorScheme } from "@/hooks/useColorScheme";

const ProfileScreen = () => {
  const router = useRouter();
  const colorScheme = useColorScheme();
  const tintColor = '#1A434F'
  //Colors[colorScheme ?? "light"].tint;

  return (
    <View className="flex-1 bg-white">
      {/* Profile Section */}
       {/* <View className="bg-black h-1/2 p-6"> */}
        {/* <View className="items-center mt-8">
          <Image
            // source={{ uri: "/api/placeholder/100/100" }}
            className="w-24 h-24 rounded-full"
          /> */}
          {/* <Text className="text-white text-xl font-bold mt-4">Test user</Text>
          <Text className="text-gray-300 mt-1">test.user@gmail.com</Text>
        </View> */}
       {/* </View> */}

      {/* Menu Items */}
      <View className="p-6">
        {/* Balance */}
        <View className="flex-row items-center mb-4 bg-[#F5F6FA] p-4 rounded-xl">
          <IconSymbol size={28} name="dollarsign.circle.fill" color={tintColor} />
          <View className="ml-4">
            <Text className="text-lg font-semibold">Balance</Text>
            <Text className="text-gray-600">1,234.56</Text>
          </View>
        </View>

        {/* Notifications */}
        <View className="flex-row items-center mb-4 bg-[#F5F6FA] p-4 rounded-xl">
          <IconSymbol size={28} name="bell.fill" color={tintColor} />
          <View className="ml-4">
            <Text className="text-lg font-semibold">Notifications</Text>
          </View>
        </View>

        {/* Customer Support */}
        <View className="flex-row items-center mb-4 bg-[#F5F6FA] p-4 rounded-xl">
          <IconSymbol size={28} name="info.circle" color={tintColor} />
          <View className="ml-4">
            <Text className="text-lg font-semibold">Customer Support</Text>
          </View>
        </View>

        {/* Logout */}
        <View className="flex-row items-center mb-4 bg-[#F5F6FA] p-4 rounded-xl">
          <IconSymbol size={28} name="rectangle.portrait.and.arrow.right" color="red" />
          <View className="ml-4">
            <Text className="text-lg font-semibold">Logout</Text>
          </View>
        </View>
      </View>
    </View>
  );
};

export default ProfileScreen;