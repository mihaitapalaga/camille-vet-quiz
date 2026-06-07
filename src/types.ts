export type Question = {
  question: string;
  answer: string;
  answers?: string[];
  multiSelect?: boolean;
  choices: readonly [string, string, string, string];
  context: string;
  source: "fractures" | "tumeurs_osseuses" | "rupture_lccr";
  type: string;
};

export const SOURCE_LABELS: Record<Question["source"], string> = {
  fractures: "Traitement des fractures",
  tumeurs_osseuses: "Tumeurs osseuses",
  rupture_lccr: "Rupture du LCCR",
};

export const SOURCE_KEYS = Object.keys(SOURCE_LABELS) as Question["source"][];

export const CHOICE_LABELS = ["A", "B", "C", "D"] as const;
export type ChoiceLabel = (typeof CHOICE_LABELS)[number];
