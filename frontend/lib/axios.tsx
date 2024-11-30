import axios, {
  AxiosError,
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse,
} from "axios";
import { createContext, ReactNode, useState } from "react";
import { type User } from "./types";

export type AxiosContextType = {
  axios: AxiosInstance;
  setToken: (token: string) => void;
  setRefreshToken: (refreshToken: string) => void;
  setUser: (user: User) => void;
  user: User | null;
};

export const axiosContext = createContext<AxiosContextType | null>(null);

export function AxiosProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);

  const axiosInstance = axios.create({
    baseURL: `http://${process.env.EXPO_PUBLIC_SERVER_URL}`,
  });

  console.log("Token");
  console.log(token);
  console.log("Refresh");
  console.log(refreshToken);
  // console.log(process.env.EXPO_PUBLIC_SERVER_URL);

  axiosInstance.interceptors.request.use(
    (config) => {
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error),
  );

  axiosInstance.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
      const originalRequest = error.config as AxiosRequestConfig & {
        _retry?: boolean;
      };
      if (
        error.response?.status === 401 &&
        !originalRequest._retry &&
        refreshToken
      ) {
        originalRequest._retry = true;
        await axios
          .get(`${process.env.EXPO_PUBLIC_SERVER_URL}/refresh`, {
            headers: {
              Authorization: `Bearer ${refreshToken}`,
            },
          })
          .then((response) => {
            setToken(response.data.token);
            setRefreshToken(response.data.refreshToken);
            return axiosInstance(originalRequest);
          })
          .catch((error) => {
            console.error(error);
            setToken(null);
            setRefreshToken(null);
          });
      }
      return Promise.reject(error);
    },
  );

  if (user === null && token !== null) {
    axiosInstance
      .get("/api/auth/user/")
      .then((response: AxiosResponse) => {
        // console.log(response.data);
        setUser(response.data);
      })
      .catch((e) => {
        if (e instanceof AxiosError) {
          console.error(e.toJSON());
        }
      });
  }
  return (
    <axiosContext.Provider
      value={{ axios: axiosInstance, setToken, setRefreshToken, user, setUser }}
    >
      {children}
    </axiosContext.Provider>
  );
}
