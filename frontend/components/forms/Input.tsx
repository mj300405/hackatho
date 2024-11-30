import { Dispatch, SetStateAction } from "react";
import { TextInput, Text, View } from "react-native";

type InputProps = {
  onChangeText: Dispatch<SetStateAction<string>>;
  value: string;
  label: string;
};

export default function Input(props: InputProps) {
  return (
    <View>
      <Text>{props.label}</Text>
      <TextInput className="border border-solid border-red-500" />
    </View>
  );
}
