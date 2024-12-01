import TinderCardWrapper from "@/components/tinder/Card";
import { AxiosContextType, axiosContext } from "@/lib/axios";
import { AxiosError, AxiosResponse } from "axios";
import { useContext, useEffect, useState } from "react";
import { View, Text } from "react-native";
import TinderCard from "react-tinder-card";
import { HobbyType, Direction } from "@/lib/types";
import { router } from "expo-router";

export default function Tinder() {
  const authContext = useContext(axiosContext) as AxiosContextType;

  const [creatingRecomendations, setCreatingRecomendations] =
    useState<boolean>(true);

  const [cards, setCards] = useState<HobbyType[]>([]);
  const [selectedCards, setSelectedCards] = useState<number[]>([]);
  const [cardsSwiped, setCardsSwiped] = useState<number>(0);

  // Retriev created recomendations from the server
  const fetchRecomendations = () => {
    console.log("Fetching recomendations");
    authContext.axios
      .get(`/api/recommendations/initial/${authContext.user?.id}/`)
      .then((response: AxiosResponse) => {
        setCards(response.data.recommendations);
      })
      .catch((e) => {
        if (e instanceof AxiosError) {
          console.error(e.response?.data);
        }
      });
  };

  // Call an endpoint to create recomendations on the server
  const createRecomendations = () => {
    console.log("Creating recomendations");
    authContext.axios
      .post(
        `http://${process.env.EXPO_PUBLIC_SERVER_URL}/api/recommendations/initial/${authContext.user?.id}/`,
      )
      .then((response: AxiosResponse) => {
        setCreatingRecomendations(false);
        fetchRecomendations();
      })
      .catch((e) => {
        if (e instanceof AxiosError) {
          if (
            e.response?.data.error ===
            "Initial recommendations already generated"
          ) {
            setCreatingRecomendations(false);
            fetchRecomendations();
          } else {
            console.error(e.response?.data);
          }
        }
      });
  };

  // Call an endpoint to create recomendations on the server
  const createRecomendations = () => {
    console.log("Creating recomendations");
    authContext.axios
      .post(
        `http://${process.env.EXPO_PUBLIC_SERVER_URL}/api/recommendations/initial/${authContext.user?.id}/`,
      )
      .then((response: AxiosResponse) => {
        setCreatingRecomendations(false);
        fetchRecomendations();
      })
      .catch((e) => {
        if (e instanceof AxiosError) {
          if (
            e.response?.data.error ===
            "Initial recommendations already generated"
          ) {
            setCreatingRecomendations(false);
            fetchRecomendations();
          } else {
            console.error(e.response?.data);
          }
        }
      });
  };

  // Call an endpoint to create recomendations on the server
  const createRecomendations = () => {
    console.log("Creating recomendations");
    authContext.axios
      .post(
        `http://${process.env.EXPO_PUBLIC_SERVER_URL}/api/recommendations/initial/${authContext.user?.id}/`,
      )
      .then((response: AxiosResponse) => {
        setCreatingRecomendations(false);
        fetchRecomendations();
      })
      .catch((e) => {
        if (e instanceof AxiosError) {
          if (
            e.response?.data.error ===
            "Initial recommendations already generated"
          ) {
            setCreatingRecomendations(false);
            fetchRecomendations();
          } else {
            console.error(e.response?.data);
          }
        }
      });
  };

  // Call an endpoint to create recomendations on the server
  const createRecomendations = () => {
    console.log("Creating recomendations");
    authContext.axios
      .post(
        `http://${process.env.EXPO_PUBLIC_SERVER_URL}/api/recommendations/initial/${authContext.user?.id}/`,
      )
      .then((response: AxiosResponse) => {
        setCreatingRecomendations(false);
        fetchRecomendations();
      })
      .catch((e) => {
        if (e instanceof AxiosError) {
          console.error(e.response?.data);
        }
      });
  };

  useEffect(() => {
    (async () => {
      createRecomendations();
    })();
  }, []);

  const handleSwipe = (direction: Direction, id: number) => {
    setCardsSwiped((prev) => prev + 1);
    if (direction === "right") {
      const newSelectedCards = [...selectedCards, id];
      setSelectedCards(newSelectedCards);
    }
  };

  useEffect(() => {
    console.log(cardsSwiped);
    if (cardsSwiped === cards.length && cards.length > 0) {
      console.log("All cards swiped.");
      const data = selectedCards.map((card) => {
        return {
          hobby_id: card,
          status: "favorite",
        };
      });
      authContext.axios
        .patch("/api/hobbies/hobbies/status/", data)
        .then((response: AxiosResponse) => {
          console.log(response.data);
          router.navigate("/(tabs)");
        })
        .catch((e) => {
          if (e instanceof AxiosError) {
            console.log(e.response?.data);
          }
        });
    }
  }, [cardsSwiped]);

  return (
    <View className="h-screen flex flex-col items-center bg-white w-screen">
      <Text>Tinder🔥</Text>
      <View className="h-full w-96 flex flex-col justify-center items-center bg-white">
        {/* Show loding when getting the messages (takes a bit of time) */}
        {creatingRecomendations && <Text>Creating recomendations...</Text>}
        {/* Show the tinder swiper when the data is ready */}
        {creatingRecomendations === false &&
          cards.map((card, index) => {
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
