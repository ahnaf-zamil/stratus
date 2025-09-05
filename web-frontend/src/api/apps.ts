/**
 * Functions for calling "Application" related API endpoints.
 */

import { apiClient, APPS_ROUTE, safeApiCall } from ".";
import type { RuntimeConfig } from "./interfaces";

const getAppRuntimes = () =>
  safeApiCall<RuntimeConfig[]>(apiClient.get(`${APPS_ROUTE}/runtimes`));

const createApplication = (name: string, runtime: string) =>
  safeApiCall<any>(
    apiClient.post(APPS_ROUTE + "/create", { name, runtime }),
  );

export const appsApi = {
  getAppRuntimes,
  createApplication,
}