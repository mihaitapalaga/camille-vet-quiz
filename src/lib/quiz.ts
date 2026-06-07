import courseQuestions from "../data/questions.json";
import objectifQuestions from "../data/objectifs_questions.json";
import type { Question } from "../types";
import { shuffleChoices } from "./shuffle";

export const COURSE_QUESTION_BANK = dedupeQuestions(courseQuestions as unknown as Question[]);
export const OBJECTIF_QUESTION_BANK = dedupeQuestions(objectifQuestions as unknown as Question[]);
export const ALL_QUESTION_BANK = dedupeQuestions([
  ...(courseQuestions as unknown as Question[]),
  ...(objectifQuestions as unknown as Question[]),
]);

export type QuestionFilter = {
  source?: Question["source"];
  objectifsOnly?: boolean;
};

const MIN_CHOICES = 4;

export function getPlayableQuestions(questions: Question[]): Question[] {
  return questions.filter((question) => hasValidChoices(question));
}

export function filterQuestions({ source, objectifsOnly = false }: QuestionFilter): Question[] {
  const bank = objectifsOnly ? OBJECTIF_QUESTION_BANK : ALL_QUESTION_BANK;
  const scoped = !source ? bank : bank.filter((question) => question.source === source);
  return dedupeQuestions(getPlayableQuestions(scoped));
}

export function dedupeQuestions(questions: Question[]): Question[] {
  const seen = new Set<string>();
  return questions.filter((question) => {
    const key = normalizeAnswer(question.question);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

export function isMultiSelectQuestion(question: Question): boolean {
  return question.multiSelect === true || (question.answers?.length ?? 0) > 1;
}

export function getCorrectAnswers(question: Question): string[] {
  if (question.answers?.length) return question.answers;
  return [question.answer];
}

export function areSelectionsCorrect(selected: readonly string[], question: Question): boolean {
  const expected = getCorrectAnswers(question).map(normalizeAnswer).sort();
  const picked = [...selected].map(normalizeAnswer).sort();
  return expected.length === picked.length && expected.every((value, index) => value === picked[index]);
}

function hasValidChoices(question: Question): boolean {
  const unique = new Set(question.choices.map((choice) => normalizeAnswer(choice)));
  return question.choices.length >= MIN_CHOICES && unique.size >= MIN_CHOICES;
}

function buildFallbackChoices(question: Question, pool: Question[]): Question["choices"] {
  const distractors: string[] = [];
  const seen = new Set(getCorrectAnswers(question).map(normalizeAnswer));

  for (const candidate of pool) {
    if (candidate.source !== question.source) continue;
    for (const value of getCorrectAnswers(candidate)) {
      const key = normalizeAnswer(value);
      if (seen.has(key)) continue;
      distractors.push(value);
      seen.add(key);
      if (distractors.length >= MIN_CHOICES - 1) break;
    }
    if (distractors.length >= MIN_CHOICES - 1) break;
  }

  const choices = [...distractors.slice(0, MIN_CHOICES - 1), ...getCorrectAnswers(question)];
  return shuffleChoices(choices.slice(0, MIN_CHOICES)) as unknown as Question["choices"];
}

function normalizeQuestionChoices(question: Question, pool: Question[]): Question {
  if (hasValidChoices(question)) {
    return {
      ...question,
      choices: shuffleChoices([...question.choices]) as unknown as Question["choices"],
    };
  }
  return {
    ...question,
    choices: buildFallbackChoices(question, pool),
  };
}

export function pickRandomQuestion(current?: Question): Question {
  return pickRandomQuestionFromPool(ALL_QUESTION_BANK, current);
}

export function pickRandomQuestionFromPool(pool: Question[], current?: Question): Question {
  const validPool = getPlayableQuestions(pool);
  if (validPool.length === 0) throw new Error("Aucune question disponible pour cette selection.");

  if (validPool.length === 1) {
    return normalizeQuestionChoices(validPool[0], validPool);
  }

  let next = validPool[Math.floor(Math.random() * validPool.length)];
  let attempts = 0;
  while (current && next.question === current.question && attempts < 10) {
    next = validPool[Math.floor(Math.random() * validPool.length)];
    attempts += 1;
  }

  return normalizeQuestionChoices(next, validPool);
}

export function normalizeAnswer(value: string): string {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

export function isAnswerCorrect(input: string, expected: string): boolean {
  return normalizeAnswer(input) === normalizeAnswer(expected);
}
