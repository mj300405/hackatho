import { ScrollView, Text } from "react-native";
import HobbyCard from "@/components/ui/HobbyCard";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { useLayoutEffect, useState, useContext } from "react";
import { axiosContext, AxiosContextType } from "@/lib/axios";

export default function Explore() {
  const [hobbies, setHobbies] = useState([]);
  const { axios } = useContext(axiosContext) as AxiosContextType;

  useLayoutEffect(() => {
    axios
      .get(`/api/recommendations/explore/`)
      .then((res) => {
        console.log(res.data);
        setHobbies(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

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
