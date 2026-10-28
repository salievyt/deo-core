/** Add approved partner names and local logo paths here. Null logos render placeholders. */
export type Partner = { id: string; name: string; logo: string | null };
export const partners: Partner[] = Array.from({ length: 6 }, (_, index) => ({
  id: `partner-${index + 1}`,
  name: `Партнёр ${String(index + 1).padStart(2, "0")}`,
  logo: null,
}));
