import { ThemedText } from "@/components/ThemedText";
import { useContext, useEffect, useState } from "react";
import { axiosContext, AxiosContextType } from "@/lib/axios";
import { HobbyType, UserHobby } from "@/lib/types";

import { View, Text, Pressable, ScrollView } from "react-native";
import { AxiosError, AxiosResponse } from "axios";
import Card from "@/components/home/Card";

export default function Home() {
  const authContext = useContext(axiosContext) as AxiosContextType;
  const [activeHobbies, setActiveHobbies] = useState<UserHobby[]>([]);
  useEffect(() => {
    authContext.axios
      .get("/api/hobbies/user/hobbies/")
      .then((response: AxiosResponse) => {
        console.log(response.data.hobbies.active);
        setActiveHobbies(response.data.hobbies.active);
      })
      .catch((e) => {
        if (e instanceof AxiosError) {
          console.error(e.response?.data);
        }
      });
  }, []);
  return (
    <View>
      <Text className="text-center font-bold text-3xl mx-5 px-5">HOME</Text>
      <ScrollView>
        {activeHobbies.map((userHobby) => {
          console.log(userHobby);
          return <Card hobby={userHobby} key={userHobby.id} />;
        })}
      </ScrollView>
    </View>
  );
}
