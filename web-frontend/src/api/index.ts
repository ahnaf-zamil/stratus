/**
 * Axios client and utility for safely calling API endpoints.
 * Includes base route constants and a generic error-handling wrapper.
 */

import axios, { type AxiosResponse } from "axios";
import type { APIResponse } from "./interfaces";

// Base API URL and route constants
const API_URL = "http://localhost:5000";
export const APPS_ROUTE = `${API_URL}/apps`;

// Configured Axios instance with credentials
export const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true,
});

/**
 * Wraps an Axios promise and returns a tuple of [data, error].
 * Ensures consistent error handling across API calls.
 */
export async function safeApiCall<T>(
  promise: Promise<AxiosResponse<APIResponse<T>>>,
): Promise<[APIResponse<T> | null, unknown]> {
  try {
    const res = await promise;
    return [res.data, null];
  } catch (error) {
    return [null, error];
  }
}
