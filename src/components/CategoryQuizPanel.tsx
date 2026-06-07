import { useMemo, useState } from "react";
import { QuizPanel } from "./QuizPanel";
import { filterQuestions } from "../lib/quiz";
import type { Question } from "../types";
import { SOURCE_KEYS, SOURCE_LABELS } from "../types";

type CategoryQuizPanelProps = {
  prizeCount: number;
  prizeMax: number;
  onCorrectAnswer: () => void;
};

type QuizMode = "course" | "objectifs";

export function CategoryQuizPanel({ prizeCount, prizeMax, onCorrectAnswer }: CategoryQuizPanelProps) {
  const [source, setSource] = useState<Question["source"]>("fractures");
  const [mode, setMode] = useState<QuizMode>("course");

  const questions = useMemo(
    () => filterQuestions({ source, objectifsOnly: mode === "objectifs" }),
    [source, mode],
  );

  return (
    <section className="category-panel">
      <div className="panel filters-panel">
        <h2>Choisis ta categorie</h2>
        <p className="filters-help">Selectionne un cours et le type de questions que tu veux reviser.</p>
        <p className="filters-count">{questions.length} questions dans cette selection</p>

        <div className="filter-group">
          <p className="filter-label">Cours</p>
          <div className="chip-row" role="group" aria-label="Categories de cours">
            {SOURCE_KEYS.map((key) => (
              <button
                key={key}
                type="button"
                className={source === key ? "chip active" : "chip"}
                onClick={() => setSource(key)}
              >
                {SOURCE_LABELS[key]}
              </button>
            ))}
          </div>
        </div>

        <div className="filter-group">
          <p className="filter-label">Type de questions</p>
          <div className="chip-row" role="group" aria-label="Type de questions">
            <button
              type="button"
              className={mode === "course" ? "chip active" : "chip"}
              onClick={() => setMode("course")}
            >
              Toutes les questions
            </button>
            <button
              type="button"
              className={mode === "objectifs" ? "chip active" : "chip"}
              onClick={() => setMode("objectifs")}
            >
              Objectifs d apprentissage
            </button>
          </div>
        </div>
      </div>

      <QuizPanel
        questions={questions}
        prizeCount={prizeCount}
        prizeMax={prizeMax}
        onCorrectAnswer={onCorrectAnswer}
        emptyMessage={`Aucune question ${mode === "objectifs" ? "d objectif d apprentissage" : ""} pour ${SOURCE_LABELS[source]}.`}
      />
    </section>
  );
}
