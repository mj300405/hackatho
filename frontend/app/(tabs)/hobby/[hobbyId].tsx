import { Text, View } from "react-native";
import { useLocalSearchParams } from "expo-router";
import { useEffect, useContext } from "react";
import { AxiosContextType, axiosContext } from "@/lib/axios";
import { AxiosError, AxiosResponse } from "axios";

export default function HobbyDetails() {
  const params = useLocalSearchParams();
  const authContext = useContext(axiosContext) as AxiosContextType;

  useEffect(() => {
    authContext.axios
      .get(`/api/hobbies/${params.hobbyId}/`)
      .then((response: AxiosResponse) => {
        console.log(response.data);
      })
      .catch((e) => {
        if (e instanceof AxiosError) {
          console.log(e.response?.data);
        }
      });
  }, []);
  return (
    <View>
      <Text>{params.hobbyId}</Text>
    </View>
  );
}
