import { useCallback, useEffect, useMemo, useState } from "react";
import type { Question } from "../types";
import { CHOICE_LABELS, SOURCE_LABELS } from "../types";
import {
  areSelectionsCorrect,
  getCorrectAnswers,
  isAnswerCorrect,
  isMultiSelectQuestion,
  normalizeAnswer,
  getPlayableQuestions,
  pickRandomQuestionFromPool,
} from "../lib/quiz";

type QuizPanelProps = {
  questions: Question[];
  prizeCount: number;
  prizeMax: number;
  onCorrectAnswer: () => void;
  emptyMessage?: string;
};

type Feedback = "idle" | "correct" | "wrong";

export function QuizPanel({
  questions,
  prizeCount,
  prizeMax,
  onCorrectAnswer,
  emptyMessage = "Aucune question disponible pour cette selection.",
}: QuizPanelProps) {
  const pool = useMemo(() => getPlayableQuestions(questions), [questions]);
  const [current, setCurrent] = useState<Question | null>(null);
  const [selected, setSelected] = useState<string[]>([]);
  const [feedback, setFeedback] = useState<Feedback>("idle");
  const [score, setScore] = useState({ correct: 0, answered: 0 });
  const [showContext, setShowContext] = useState(false);

  const multiSelect = current ? isMultiSelectQuestion(current) : false;
  const correctAnswers = current ? getCorrectAnswers(current) : [];

  useEffect(() => {
    if (pool.length === 0) {
      setCurrent(null);
      return;
    }
    setCurrent(pickRandomQuestionFromPool(pool));
    setSelected([]);
    setFeedback("idle");
    setShowContext(false);
  }, [pool]);

  const loadNext = useCallback(() => {
    if (pool.length === 0) return;
    setCurrent((prev) => pickRandomQuestionFromPool(pool, prev ?? undefined));
    setSelected([]);
    setFeedback("idle");
    setShowContext(false);
  }, [pool]);

  const selectSingleChoice = (choice: string) => {
    if (!current || feedback !== "idle" || multiSelect) return;
    setSelected([choice]);
    const ok = isAnswerCorrect(choice, current.answer);
    setFeedback(ok ? "correct" : "wrong");
    setScore((prev) => ({
      correct: prev.correct + (ok ? 1 : 0),
      answered: prev.answered + 1,
    }));
    if (ok) onCorrectAnswer();
    setShowContext(true);
  };

  const toggleMultiChoice = (choice: string) => {
    if (!current || feedback !== "idle" || !multiSelect) return;
    setSelected((prev) => {
      const key = normalizeAnswer(choice);
      const exists = prev.some((item) => normalizeAnswer(item) === key);
      if (exists) return prev.filter((item) => normalizeAnswer(item) !== key);
      return [...prev, choice];
    });
  };

  const submitMultiChoice = () => {
    if (!current || feedback !== "idle" || !multiSelect || selected.length === 0) return;
    const ok = areSelectionsCorrect(selected, current);
    setFeedback(ok ? "correct" : "wrong");
    setScore((prev) => ({
      correct: prev.correct + (ok ? 1 : 0),
      answered: prev.answered + 1,
    }));
    if (ok) onCorrectAnswer();
    setShowContext(true);
  };

  const isChoiceSelected = (choice: string) =>
    selected.some((item) => normalizeAnswer(item) === normalizeAnswer(choice));

  const isChoiceCorrect = (choice: string) =>
    correctAnswers.some((answer) => isAnswerCorrect(choice, answer));

  const choiceClass = (choice: string) => {
    if (!current) return "choice-btn";
    if (feedback === "idle") {
      return multiSelect && isChoiceSelected(choice) ? "choice-btn selected" : "choice-btn";
    }
    if (isChoiceCorrect(choice)) return "choice-btn correct";
    if (isChoiceSelected(choice)) return "choice-btn wrong";
    return "choice-btn";
  };

  const prizeProgress = (prizeCount / prizeMax) * 100;

  if (!current) {
    return (
      <section className="panel quiz-panel">
        <p className="empty-state">{emptyMessage}</p>
      </section>
    );
  }

  const typeLabel = current.type === "objectif_apprentissage" ? "Objectif d'apprentissage" : "Question de cours";
  const expectedLabel = correctAnswers.join(" ? ");

  return (
    <section className="panel quiz-panel">
      <div className="panel-top">
        <div className="badge-row">
          <span className="badge">{SOURCE_LABELS[current.source]}</span>
          <span className="badge badge-soft">{typeLabel}</span>
          {multiSelect && <span className="badge badge-soft">Sélection multiple</span>}
        </div>
        <span className="meta">{pool.length} questions disponibles</span>
      </div>

      <div className="prize-progress-card">
        <p className="prize-progress-label">Compteur grand prix : {prizeCount}/{prizeMax}</p>
        <div className="progress-track" aria-hidden="true">
          <div className="progress-fill" style={{ width: `${prizeProgress}%` }} />
        </div>
      </div>

      <p className="question-text">{current.question}</p>
      {multiSelect && (
        <p className="multi-hint">Sélectionne toutes les bonnes réponses, puis clique sur Valider.</p>
      )}

      <div className="choices-grid" role="group" aria-label="Choix de réponse A B C D">
        {current.choices.map((choice, index) => (
          <button
            key={`${current.question}-${index}`}
            type="button"
            className={choiceClass(choice)}
            onClick={() => (multiSelect ? toggleMultiChoice(choice) : selectSingleChoice(choice))}
            disabled={feedback !== "idle"}
            aria-pressed={multiSelect ? isChoiceSelected(choice) : undefined}
          >
            <span className="choice-label">{CHOICE_LABELS[index]}</span>
            <span className="choice-text">{choice}</span>
          </button>
        ))}
      </div>

      {multiSelect && feedback === "idle" && (
        <div className="submit-row">
          <button
            type="button"
            className="submit-btn"
            onClick={submitMultiChoice}
            disabled={selected.length === 0}
          >
            Valider ma réponse
          </button>
        </div>
      )}

      {feedback !== "idle" && (
        <div className={`feedback ${feedback}`}>
          {feedback === "correct"
            ? "Correct ! +1 sur le compteur grand prix"
            : `Incorrect. ${multiSelect ? "Les bonnes réponses étaient" : "La bonne réponse était"} : ${expectedLabel}`}
        </div>
      )}

      {showContext && (
        <p className="context">
          <strong>Extrait du cours :</strong> {current.context}
        </p>
      )}

      <div className="panel-footer">
        <p className="score">
          Score : {score.correct}/{score.answered}
        </p>
        <button type="button" className="secondary" onClick={loadNext}>
          Question suivante
        </button>
      </div>
    </section>
  );
}
