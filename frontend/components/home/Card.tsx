import { UserHobby } from "@/lib/types";
import React from "react";
import { View, Text, Pressable } from "react-native";
import { router } from "expo-router";

type CardProps = {
  hobby: UserHobby;
};

export default function Card(props: CardProps) {
  return (
    <Pressable
      className="bg-white p-4 rounded-lg shadow-md w-full mb-4"
      onPress={() => {
        router.push(`/hobby/${props.hobby.hobby.id}`);
      }}
    >
      <Text className="text-lg font-bold text-gray-800">
        {props.hobby.hobby.name}
      </Text>
      <Text className="text-sm text-gray-600">
        {props.hobby.hobby.category.name}
      </Text>

      <View className="mt-2">
        <Text className="text-sm font-semibold text-gray-700">Status:</Text>
        <Text className="text-sm text-gray-600">{props.hobby.status}</Text>
      </View>

      <View className="mt-2">
        <Text className="text-sm font-semibold text-gray-700">Difficulty:</Text>
        <Text className="text-sm text-gray-600">
          {props.hobby.hobby.difficulty_level}
        </Text>
      </View>

      <View className="mt-2">
        <Text className="text-sm font-semibold text-gray-700">
          Days Active:
        </Text>
        <Text className="text-sm text-gray-600">{props.hobby.days_active}</Text>
      </View>

      <View className="mt-2">
        <Text className="text-sm font-semibold text-gray-700">
          Last Activity:
        </Text>
        <Text className="text-sm text-gray-600">
          {new Date(props.hobby.last_activity).toLocaleDateString()}
        </Text>
      </View>
    </Pressable>
  );
}
