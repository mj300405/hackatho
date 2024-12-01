import { Text, View } from "react-native";
import { useLocalSearchParams } from "expo-router";
import { useEffect, useContext, useState } from "react";
import { AxiosContextType, axiosContext } from "@/lib/axios";
import { AxiosError, AxiosResponse } from "axios";
import { UserHobby } from "@/lib/types";

export default function HobbyDetails() {
  const params = useLocalSearchParams();
  const authContext = useContext(axiosContext) as AxiosContextType;
  const [userHobby, setUserHobby] = useState<UserHobby | null>(null);

  useEffect(() => {
    authContext.axios
      .get(`/api/hobbies/${params.hobbyId}/`)
      .then((response: AxiosResponse) => {
        console.log(response.data);
        setUserHobby(response.data);
      })
      .catch((e) => {
        if (e instanceof AxiosError) {
          console.log(e.response?.data);
        }
      });
  }, []);
  if (userHobby === null) {
    return (
      <View>
        <Text>Loading</Text>
      </View>
    );
  } else
    return (
      <View className="bg-white p-6 rounded-xl shadow-md border border-gray-200 space-y-4 h-screen">
        {/* Header Section */}
        <View>
          <Text className="text-2xl font-bold text-gray-800">
            {userHobby.hobby.name}
          </Text>
          <Text className="text-sm text-gray-600 mt-1">
            {userHobby.hobby.description}
          </Text>
        </View>

        {/* Category Section */}
        <View>
          <Text className="text-base font-semibold text-gray-700">
            Category
          </Text>
          <Text className="text-sm text-gray-600">
            {userHobby.hobby.category.name}
          </Text>
          <Text className="text-xs text-gray-500">
            {userHobby.hobby.category.description}
          </Text>
        </View>

        {/* Details Section */}
        <View>
          <Text className="text-base font-semibold text-gray-700">Details</Text>
          <View className="space-y-1 mt-2">
            <Text className="text-sm text-gray-600">
              <Text className="font-semibold">Difficulty:</Text>{" "}
              {userHobby.hobby.difficulty_level}
            </Text>
            <Text className="text-sm text-gray-600">
              <Text className="font-semibold">Minimum Age:</Text>{" "}
              {userHobby.hobby.minimum_age}
            </Text>
            <Text className="text-sm text-gray-600">
              <Text className="font-semibold">Price Range:</Text>{" "}
              {userHobby.hobby.price_range}
            </Text>
            <Text className="text-sm text-gray-600">
              <Text className="font-semibold">Time Commitment:</Text>{" "}
              {userHobby.hobby.time_commitment} hrs/week
            </Text>
          </View>
        </View>

        {/* Required Equipment Section */}
        <View>
          <Text className="text-base font-semibold text-gray-700">
            Required Equipment
          </Text>
          {userHobby.hobby.required_equipment.length > 0 ? (
            userHobby.hobby.required_equipment.map((item, index) => (
              <Text key={index} className="text-sm text-gray-800">
                - {item}
              </Text>
            ))
          ) : (
            <Text className="text-sm text-gray-500">None</Text>
          )}
        </View>

        {/* Progress Section */}
        <View>
          <Text className="text-base font-semibold text-gray-700">
            Progress
          </Text>
          <View className="space-y-1 mt-2">
            <Text className="text-sm text-gray-600">
              <Text className="font-semibold">Days Active:</Text>{" "}
              {userHobby.days_active}
            </Text>
            <Text className="text-sm text-gray-600">
              <Text className="font-semibold">Status:</Text> {userHobby.status}
            </Text>
            <Text className="text-sm text-gray-600">
              <Text className="font-semibold">Last Activity:</Text>{" "}
              {new Date(userHobby.last_activity).toLocaleDateString()}
            </Text>
            <Text className="text-sm text-gray-600">
              <Text className="font-semibold">Started At:</Text>{" "}
              {new Date(userHobby.started_at).toLocaleDateString()}
            </Text>
          </View>
        </View>

        {/* Notes Section */}
        {userHobby.notes && (
          <View>
            <Text className="text-base font-semibold text-gray-700">Notes</Text>
            <Text className="text-sm text-gray-600 mt-2">
              {userHobby.notes}
            </Text>
          </View>
        )}
      </View>
    );
}
