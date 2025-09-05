/**
 * Generic wrapper for API responses.
 * Used to type responses from safeApiCall<T>.
 */
export interface APIResponse<T> {
  data: T;
  error: boolean;
}

/**
 * Represents a runtime configuration returned by the API.
 * Used to populate the runtime selection dropdown.
 */
export interface RuntimeConfig {  
  id: string;
  version: string;
  language: string;
}
