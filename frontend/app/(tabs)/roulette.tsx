import { ScrollView, StyleSheet, Button, View, Text } from "react-native";
import { useLayoutEffect, useState } from "react";
import W3CtextColor from "@/lib/W3CTextColor";

export default function App() {
  const finalElement = {
    color: {
      red: 255,
      green: 255,
      blue: 255,
      textColor: `#000000`,
      style: `rgb(255, 255, 255)`,
    },
  };

  const colors = [
    { red: 26, green: 67, blue: 79 },
    { red: 195, green: 244, blue: 77 },
    { red: 97, green: 211, blue: 131 },
    { red: 211, green: 194, blue: 248 },
    { red: 250, green: 243, blue: 235 },
    { red: 234, green: 250, blue: 239 },
    { red: 245, green: 246, blue: 250 },
  ];

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
    const time = 2000; // 2 seconds
    const start = Date.now();
    const interval = setInterval(() => {
      const elapsed = Date.now() - start;
      if (elapsed >= time) {
        clearInterval(interval);
        setColor(finalElement.color);
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
          className="w-[90%] aspect-square rounded-2xl"
          style={{ backgroundColor: color.style, padding: 20 }}
        >
          <Text style={{ color: color.textColor }}>
            L∷ᒷᒲ ╎!¡ᓭ⚍ᒲ ↸𝙹ꖎ𝙹∷ ᓭ╎ℸ ̣ , ᔑᒲᒷℸ ̣ ᓵ𝙹リᓭᒷᓵℸ ̣ ᒷℸ ̣ ⚍∷ ᔑ↸╎!¡╎ᓭ╎ᓵ╎リ⊣ ᒷꖎ╎ℸ
            ̣. O!¡ℸ ̣ ╎𝙹, ᔑ∷ᓵ⍑╎ℸ ̣ ᒷᓵℸ ̣
          </Text>
        </View>
      </View>
      <Button title="Spin" onPress={spin} />
    </View>
  );
}
