import { View, Text } from "react-native";

type TinderCardWrapperProps = {
  children: string | string[];
};

export default function TinderCardWrapper(props: TinderCardWrapperProps) {
  return (
    <View className="absolute left-[-80px] w-40 h-72 top-[-144px] bg-slate-300 flex justify-center items-center rounded-xl">
      <Text className="text-black text-center">{props.children}</Text>
    </View>
  );
}
