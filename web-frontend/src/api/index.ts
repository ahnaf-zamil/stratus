import axios, { type AxiosResponse } from "axios";

const API_URL = "http://localhost:5000";
export const APPS_ROUTE = API_URL + "/apps";

export const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true,
});

export async function safeApiCall<T>(
  promise: Promise<AxiosResponse<T>>,
): Promise<[T | null, unknown]> {
  try {
    const res = await promise;
    return [res.data, null];
  } catch (error) {
    return [null, error];
  }
}
