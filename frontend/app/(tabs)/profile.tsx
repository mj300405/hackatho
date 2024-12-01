import { View, Text, TouchableOpacity } from "react-native";
import { useRouter } from "expo-router";
import { IconSymbol } from "@/components/ui/IconSymbol";
import { useColorScheme } from "@/hooks/useColorScheme";
import { useContext, useLayoutEffect } from "react";
import { axiosContext, AxiosContextType } from "@/lib/axios";

const ProfileScreen = () => {
  const router = useRouter();
  const tintColor = "#1A434F";
  const { setToken, setRefreshToken, refreshUser, user } = useContext(
    axiosContext,
  ) as AxiosContextType;

  const handleLogout = () => {
    // Reset the tokens
    setToken(null);
    setRefreshToken(null);

    // Navigate back to index screen
    router.replace("/login");
  };
  //Colors[colorScheme ?? "light"].tint;

  useLayoutEffect(() => {
    refreshUser();
  }, []);

  return (
    <View className="flex-1 bg-white pt-12">
      <View className="px-8">
        {/* Profile Header */}
        <View className="flex-row items-center mb-4">
          {/* Black Profile Picture Placeholder */}
          <View className="w-16 h-16 bg-black rounded-2xl" />

          {/* User Info */}
          <View className="ml-4">
            <Text className="text-xl font-bold">{user?.username}</Text>
            <Text className="text-gray-500">{user?.email}</Text>
          </View>
        </View>
        {/* Menu Items */}
        {/* Balance */}
        <View className="pt-10">
          <View className="flex-row items-center mb-4 bg-[#F5F6FA] p-4 rounded-xl">
            <IconSymbol
              size={28}
              name="dollarsign.circle.fill"
              color={tintColor}
            />
            <View className="ml-4">
              <Text className="text-lg font-semibold">Balance</Text>
              <Text className="text-gray-600">{user?.coins}</Text>
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
          <TouchableOpacity
            className="flex-row items-center mb-4 bg-[#F5F6FA] p-4 rounded-xl"
            onPress={handleLogout}
          >
            <IconSymbol
              size={28}
              name="rectangle.portrait.and.arrow.right"
              color="red"
            />
            <View className="ml-4">
              <Text className="text-lg font-semibold">Logout</Text>
            </View>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};

export default ProfileScreen;
