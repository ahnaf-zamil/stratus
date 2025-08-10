export function isEmptyString(str: string | null | undefined): boolean {
  return !str || str.trim().length === 0;
}
