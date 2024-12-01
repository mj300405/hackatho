import TinderCardWrapper from "@/components/tinder/Card";
import { AxiosContextType, axiosContext } from "@/lib/axios";
import { AxiosError, AxiosResponse } from "axios";
import { useContext, useEffect, useState } from "react";
import { View, Text } from "react-native";
import TinderCard from "react-tinder-card";
import { HobbyType, Direction } from "@/lib/types";

export default function Tinder() {
  const authContext = useContext(axiosContext) as AxiosContextType;

  // TODO: Uncomment this code to fetch recommendations from the server

  const [cards, setCards] = useState<
    (HobbyType & { direction: Direction | null })[]
  >([]);

  useEffect(() => {
    // Call an endpoint to create recomendations on the server
    authContext.axios
      .post(
        `http://${process.env.EXPO_PUBLIC_SERVER_URL}/api/recommendations/initial/${authContext.user?.id}/`,
      )
      .catch((e) => {
        if (e instanceof AxiosError) {
          console.error(e.response?.data);
        }
      });

    // Retriev created recomendations from the server
    authContext.axios
      .get(
        `http://${process.env.EXPO_PUBLIC_SERVER_URL}/api/recommendations/initial/${authContext.user?.id}/`,
      )
      .then((response: AxiosResponse) => {
        // Adding direction property to Hobby object.
        const cardsWithDir = response.data.recommendations.map(
          (hobby: HobbyType) => {
            return { ...hobby, direction: null };
          },
        );
        setCards(cardsWithDir);
      })
      .catch((e) => {
        if (e instanceof AxiosError) {
          console.error(e.response?.data);
        }
      });
  }, []);

  const handleSwipe = (direction: Direction, id: number) => {
    const newCards = [...cards];
    const swipedCard = newCards.find((c) => c.id === id);
    if (swipedCard !== undefined) swipedCard.direction = direction;
    setCards(newCards);
  };

  useEffect(() => {
    if (cards.length === 0) return;
    let allSwiped = true;
    cards.forEach((card) => {
      if (card.direction === null) {
        allSwiped = false;
      }
    });
    if (allSwiped) {
      console.log("All cards swiped.");
      // TODO: upload swiped cards somewhere and redirect somewhere
      // tylko id
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
              <TinderCardWrapper key={index}>
                {card.name} {card.difficulty_level}{" "}
                {card.minimum_age.toString()}
              </TinderCardWrapper>
            </TinderCard>
          );
        })}
      </View>
    </View>
  );
}
