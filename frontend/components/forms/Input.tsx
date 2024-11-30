import { Dispatch, SetStateAction } from "react";
import { TextInput, Text, View } from "react-native";
import InputLabel from "./InputLabel";
import { TextInputProps } from "react-native";
type InputProps<T> = {
  onChangeText: Dispatch<SetStateAction<T>>;
  value: T;
  label: string;
} & TextInputProps;

export default function Input<T>(props: InputProps<T>) {
  return (
    <View>
      <InputLabel>{props.label}</InputLabel>
      <TextInput className="border border-solid border-slate-300 rounded-xl" {...props} />
    </View>
  );
}
