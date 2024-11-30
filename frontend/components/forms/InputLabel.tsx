import { Text } from "react-native";
import clsx from "clsx";

type InputLabelProps = {
  children: string;
  className?: string;
};

export default function InputLabel(props: InputLabelProps) {
  return <Text className={clsx(["", props.className])}>{props.children}</Text>;
}
