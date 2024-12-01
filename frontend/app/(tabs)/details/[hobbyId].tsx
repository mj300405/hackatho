import { useLocalSearchParams } from "expo-router";
import { View, Text } from "react-native";
import { useContext, useLayoutEffect } from "react";
import { axiosContext, AxiosContextType } from "@/lib/axios";

export default function HobbyDetails() {
  const { hobbyId } = useLocalSearchParams();

  const { axios } = useContext(axiosContext) as AxiosContextType;

  useLayoutEffect(() => {
    axios
      .get(`/api/hobbies/${hobbyId}/`)
      .then((res) => {
        console.log(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, [hobbyId]);

  return (
    <View>
      <Text>Details {hobbyId}</Text>
    </View>
  );
}
