import { useCallback, useState } from "react";
import { PrizeCounter, PRIZE_MAX } from "./components/PrizeCounter";
import { QuizPanel } from "./components/QuizPanel";
import { ALL_QUESTION_BANK } from "./lib/quiz";
import "./App.css";

type Tab = "quiz" | "counter";

export default function App() {
  const [tab, setTab] = useState<Tab>("quiz");
  const [prizeCount, setPrizeCount] = useState(0);
  const [showPrizePopup, setShowPrizePopup] = useState(false);
  const incrementPrize = useCallback(() => {
    setPrizeCount((prev) => {
      const next = prev + 1;
      if (next >= PRIZE_MAX) {
        setShowPrizePopup(true);
        return PRIZE_MAX;
      }
      return next;
    });
  }, []);

  const resetPrize = useCallback(() => {
    setPrizeCount(0);
    setShowPrizePopup(false);
  }, []);

  const closePrizePopup = useCallback(() => {
    setShowPrizePopup(false);
    setPrizeCount(0);
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <p className="eyebrow">UC 0422 · Revision veterinaire</p>
          <h1>Bonjour Camille 👋</h1>
          <p className="subtitle">
            Questions generees uniquement a partir de tes cours (fractures, tumeurs osseuses, rupture LCCR), y compris les objectifs d apprentissage.
          </p>
        </div>
        <nav className="tabs" aria-label="Navigation principale">
          <button type="button" className={tab === "quiz" ? "tab active" : "tab"} onClick={() => setTab("quiz")}>
            Quiz aleatoire
          </button>
          <button type="button" className={tab === "counter" ? "tab active" : "tab"} onClick={() => setTab("counter")}>
            Compteur prix
          </button>
        </nav>
      </header>
      <main className="app-main">
        {tab === "quiz" && (
          <QuizPanel
            questions={ALL_QUESTION_BANK}
            prizeCount={prizeCount}
            prizeMax={PRIZE_MAX}
            onCorrectAnswer={incrementPrize}
          />
        )}
        {tab === "counter" && (
          <PrizeCounter
            count={prizeCount}
            onIncrement={incrementPrize}
            onReset={resetPrize}
            showPopup={showPrizePopup}
            onClosePopup={closePrizePopup}
          />
        )}
      </main>

      {showPrizePopup && tab !== "counter" && (
        <div className="popup-overlay" role="dialog" aria-modal="true" aria-label="Felicitations">
          <div className="popup-card">
            <p>🎉</p>
            <h3>Congratulations Camille you won the big Prize</h3>
            <button type="button" onClick={closePrizePopup}>
              Super !
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
