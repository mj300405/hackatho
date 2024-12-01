import TinderCardWrapper from "@/components/tinder/Card";
import { AxiosContextType, axiosContext } from "@/lib/axios";
import { AxiosError, AxiosResponse } from "axios";
import { useContext, useEffect, useState } from "react";
import { View, Text } from "react-native";
import TinderCard from "react-tinder-card";

export default function Tinder() {
  const authContext = useContext(axiosContext) as AxiosContextType;

  // TODO: Uncomment this code to fetch recommendations from the server
  // authContext.axios
  //   .post(
  //     `http://${process.env.EXPO_PUBLIC_SERVER_URL}/api/recommendations/initial/${authContext.user?.id}/`,
  //   )
  //   .then((response: AxiosResponse) => {
  //     console.log(response.data);
  //   })
  //   .catch((e) => {
  //     if (e instanceof AxiosError) {
  //       console.error(e.response?.data);
  //     }
  //   });

  // TODO: move to types
  type HobbyType = {
    id: number;
    name: string;
    description: string;
    difficulty_level: string;
    time_commitment: number;
    price_range: string;
    required_equipment: string[];
    minimum_age: number;
    match_level: string;
  };

  // TODO: move to types
  type Direction = "left" | "right" | "up" | "down";

  // TODO: remove after a mock
  const cardsMock: (HobbyType & {
    direction: Direction | null;
  })[] = [
    {
      id: 1,
      name: "Swim",
      description: "Swim in the pool",
      difficulty_level: "asdasd",
      time_commitment: 1,
      price_range: "asdasd",
      required_equipment: ["asdasd"],
      minimum_age: 1,
      match_level: "asdasd",
      direction: null,
    },
    {
      id: 2,
      name: "Bike",
      description: "Bike in the park",
      difficulty_level: "asdasd",
      time_commitment: 1,
      price_range: "asdasd",
      required_equipment: ["asdasd"],
      minimum_age: 1,
      match_level: "asdasd",
      direction: null,
    },
    {
      id: 3,
      name: "Hiking",
      description: "Hiking into the mountain",
      difficulty_level: "asdasd",
      time_commitment: 1,
      price_range: "asdasd",
      required_equipment: ["asdasd"],
      minimum_age: 1,
      match_level: "asdas",
      direction: null,
    },
  ];

  const [cards, setCards] = useState(cardsMock);

  const handleSwipe = (direction: Direction, id: number) => {
    const newCards = [...cards];
    const swipedCard = newCards.find((c) => c.id === id);
    if (swipedCard !== undefined) swipedCard.direction = direction;
    setCards(newCards);
  };

  useEffect(() => {
    let allSwiped = true;
    cards.forEach((card) => {
      if (card.direction === null) {
        allSwiped = false;
      }
    });
    if (allSwiped) {
      console.log("All cards swiped.");
      // TODO: upload swiped cards somewhere and redirect somewhere
    }
  }, [cards]);

  return (
    <View className="h-screen flex flex-col items-center bg-white w-screen">
      <Text>Tinder🔥</Text>
      <View className="h-full w-96 flex flex-col justify-center items-center bg-white">
        {cards.map((card, index) => {
          return (
            <TinderCard
              key={card.id}
              preventSwipe={["up", "down"]}
              onSwipe={(dir) => {
                handleSwipe(dir, card.id);
              }}
            >
              <TinderCardWrapper key={index}>{card.name}</TinderCardWrapper>
            </TinderCard>
          );
        })}
      </View>
    </View>
  );
}
