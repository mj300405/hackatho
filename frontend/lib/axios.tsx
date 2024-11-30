import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from "axios";
import { createContext, ReactNode, useState } from "react";

export type AxiosContextType = {
  axios: AxiosInstance;
};

export const axiosContext = createContext<AxiosContextType | null>(null);

export function AxiosProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);

  const axiosInstance = axios.create({
    baseURL: process.env.EXPO_PUBLIC_SERVER_URL,
  });

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

  return (
    <axiosContext.Provider value={{ axios: axiosInstance }}>
      {children}
    </axiosContext.Provider>
  );
}
