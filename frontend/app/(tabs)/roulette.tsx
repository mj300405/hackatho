import { useContext } from "react";
import { ScrollView, StyleSheet, Button, View, Text } from "react-native";
import { useLayoutEffect, useState } from "react";
import { axiosContext, AxiosContextType } from "@/lib/axios";
import W3CtextColor from "@/lib/W3CTextColor";
import { AxiosError } from "axios";
import { router } from "expo-router";
import type { HobbyRouletteResponse } from "@/lib/types";

export default function App() {
  const { axios } = useContext(axiosContext) as AxiosContextType;

  const [text, setText] = useState<string>("Give me a spin!");
  const [showHobby, setShowHobby] = useState<boolean>(false);
  const [showSpin, setShowSpin] = useState<boolean>(true);
  const [hobby, setHobby] = useState<HobbyRouletteResponse | null>(null);

  let finalElement = {
    name: "Hobby",
    id: 0,
    color: {
      red: 255,
      green: 255,
      blue: 255,
      textColor: `#000000`,
      style: `rgb(255, 255, 255)`,
    },
  };

  const colors = [
    { red: 26, green: 67, blue: 79 }, // #1A434F
    { red: 195, green: 244, blue: 77 }, // #C3F44D
    { red: 97, green: 211, blue: 131 }, // #61D383
    { red: 211, green: 194, blue: 248 }, // #D3C2F8
    { red: 250, green: 243, blue: 235 }, // #FAF3EB
    { red: 234, green: 250, blue: 239 }, // #EAFEEF
    { red: 245, green: 246, blue: 250 }, // #F5F6FA
  ];

  const getRandomHobby = async () => {
    await axios
      .post("/api/recommendations/roulette/", {})
      .then((response) => {
        setHobby(response.data);
        console.log(response.data);
        spin();
      })
      .catch((e) => {
        //   if errorcode === 203  send message to user
        if (e instanceof AxiosError) {
          if (e.response?.status === 203) {
            setText("No spin alowed for now...");
            return;
          }
        }
        setText("An error occured!");
        console.error(e);
        throw e;
      });
  };

  useLayoutEffect(() => {
    const color = randomColor();
  }, []);

  const randomColor = () => {
    const randomItem = colors[Math.floor(Math.random() * colors.length)];
    const textColor = W3CtextColor(
      randomItem.red,
      randomItem.green,
      randomItem.blue,
    );
    return {
      red: randomItem.red,
      green: randomItem.green,
      blue: randomItem.blue,
      textColor: textColor,
      style: `rgb(${randomItem.red}, ${randomItem.green}, ${randomItem.blue})`,
    };
  };

  const [color, setColor] = useState(randomColor());

  const spin = () => {
    setText("Spinning...");
    const time = 2000; // 2 seconds
    const start = Date.now();
    const interval = setInterval(() => {
      const elapsed = Date.now() - start;
      if (elapsed >= time) {
        clearInterval(interval);
        setColor(finalElement.color);
        setShowSpin(false);
        setShowHobby(true);
        return;
      }
      setColor(randomColor());
    }, 200);
  };

  return (
    <View
      className="flex"
      style={{
        alignItems: "center",
        justifyContent: "center",
        height: "60%",
        overflow: "hidden",
      }}
    >
      <View className="flex-row justify-center">
        <View
          className="w-[90%] aspect-square rounded-2xl flex justify-center"
          style={{ backgroundColor: color.style, padding: 20 }}
        >
          <Text
            className="text-center font-bold text-2xl"
            style={{ color: color.textColor }}
          >
            {showHobby ? hobby?.recommendation.name : text}
          </Text>
        </View>
      </View>
      {showSpin && <Button title="Spin" onPress={getRandomHobby} />}
      {showHobby && (
        <Button
          title="Check out your new hobby!"
          onPress={() => {
            router.push(`/(tabs)/hobby/${hobby?.recommendation.id}`);
          }}
        />
      )}
    </View>
  );
}
