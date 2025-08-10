import { apiClient, APPS_ROUTE, safeApiCall } from ".";
import type { IRuntime } from "./interfaces";

export const getAppRuntimes = () =>
  safeApiCall<IRuntime[]>(apiClient.get(APPS_ROUTE + "/runtimes"));

export const createApplication = (name: string, runtime: string) =>
  safeApiCall<IRuntime[]>(
    apiClient.post(APPS_ROUTE + "/create", { name, runtime }),
  );
