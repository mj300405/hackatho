import { AxiosContextType, axiosContext } from "@/lib/axios";
import { AxiosError, AxiosResponse } from "axios";
import { useContext } from "react";
import { View, Text } from "react-native";
import TinderCard from "react-tinder-card";

export default function Tinder() {
  const authContext = useContext(axiosContext) as AxiosContextType;
  authContext.axios
    .get(
      `http://${process.env.EXPO_PUBLIC_SERVER_URL}/api/recommendations/initial/${authContext.user?.id}/`,
    )
    .then((response: AxiosResponse) => {
      console.log(response.data);
    })
    .catch((e) => {
      if (e instanceof AxiosError) {
        console.error(e.response?.data);
      }
    });
  return (
    <View className="h-screen bg-white flex flex-col items-center w-screen">
      <TinderCard>
        <View className="h-10">
          <Text className="text-black">Hello world</Text>
        </View>
      </TinderCard>
      <TinderCard>
        <View className="h-10">
          <Text className="text-black">Hello world</Text>
        </View>
      </TinderCard>
    </View>
  );
}
