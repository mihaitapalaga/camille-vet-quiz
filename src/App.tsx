import { useCallback, useState } from "react";
import { PrizeCounter, PRIZE_MAX } from "./components/PrizeCounter";
import { QuizPanel } from "./components/QuizPanel";
import { ALL_QUESTION_BANK } from "./lib/quiz";
import "./App.css";

type Tab = "quiz" | "counter";

const STORAGE_USER_KEY = "vetQuiz_currentUser";
const scoreKey = (user: string) => `vetQuiz_score_${user.toLowerCase().trim()}`;

function validateName(name: string): string | null {
  const trimmed = name.trim();
  if (trimmed.length === 0) return "Le prénom ne peut pas être vide.";
  if (trimmed.length > 50) return "Le prénom est trop long (50 caractères max).";
  if (!/^[a-zA-ZÀ-ÿ\s\-']+$/.test(trimmed)) return "Le prénom ne peut contenir que des lettres.";
  return null;
}

function UserPicker({ onConfirm }: { onConfirm: (name: string) => void }) {
  const [input, setInput] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const err = validateName(input);
    if (err) {
      setError(err);
      return;
    }
    setError(null);
    onConfirm(input.trim());
  };

  return (
    <div className="user-picker-overlay">
      <div className="user-picker-card">
        <p className="eyebrow">UC 0422 · Révision vétérinaire</p>
        <h1>Qui es-tu ?</h1>
        <p className="subtitle">Entre ton prénom pour sauvegarder ton score.</p>
        <form onSubmit={handleSubmit} className="user-picker-form">
          <input
            type="text"
            className="user-picker-input"
            placeholder="Ton prénom"
            value={input}
            onChange={(e) => {
              setInput(e.target.value);
              setError(null);
            }}
            maxLength={50}
            autoFocus
            autoComplete="off"
          />
          {error && <p className="user-picker-error">{error}</p>}
          <button type="submit" className="user-picker-btn">
            Commencer
          </button>
        </form>
      </div>
    </div>
  );
}

export default function App() {
  const [currentUser, setCurrentUser] = useState<string | null>(() => {
    return localStorage.getItem(STORAGE_USER_KEY);
  });

  const [tab, setTab] = useState<Tab>("quiz");

  const [prizeCount, setPrizeCount] = useState<number>(() => {
    const user = localStorage.getItem(STORAGE_USER_KEY);
    if (!user) return 0;
    return parseInt(localStorage.getItem(scoreKey(user)) || "0", 10);
  });

  const [showPrizePopup, setShowPrizePopup] = useState(false);

  const handleUserConfirm = useCallback((name: string) => {
    localStorage.setItem(STORAGE_USER_KEY, name);
    const saved = parseInt(localStorage.getItem(scoreKey(name)) || "0", 10);
    setPrizeCount(saved);
    setCurrentUser(name);
  }, []);

  const handleChangeUser = useCallback(() => {
    localStorage.removeItem(STORAGE_USER_KEY);
    setCurrentUser(null);
    setPrizeCount(0);
    setShowPrizePopup(false);
  }, []);

  const incrementPrize = useCallback(() => {
    setPrizeCount((prev) => {
      const next = Math.min(prev + 1, PRIZE_MAX);
      if (currentUser) localStorage.setItem(scoreKey(currentUser), String(next));
      if (next >= PRIZE_MAX) setShowPrizePopup(true);
      return next;
    });
  }, [currentUser]);

  const resetPrize = useCallback(() => {
    setPrizeCount(0);
    setShowPrizePopup(false);
    if (currentUser) localStorage.setItem(scoreKey(currentUser), "0");
  }, [currentUser]);

  const closePrizePopup = useCallback(() => {
    setShowPrizePopup(false);
    setPrizeCount(0);
    if (currentUser) localStorage.setItem(scoreKey(currentUser), "0");
  }, [currentUser]);

  if (!currentUser) {
    return <UserPicker onConfirm={handleUserConfirm} />;
  }

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <p className="eyebrow">UC 0422 · Révision vétérinaire</p>
          <h1>Bonjour {currentUser} 👋</h1>
          <p className="subtitle">
            Questions générées uniquement à partir de tes cours (fractures, tumeurs osseuses, rupture LCCR), y compris les objectifs d'apprentissage.
          </p>
        </div>
        <nav className="tabs" aria-label="Navigation principale">
          <button type="button" className={tab === "quiz" ? "tab active" : "tab"} onClick={() => setTab("quiz")}>
            Quiz aléatoire
          </button>
          <button type="button" className={tab === "counter" ? "tab active" : "tab"} onClick={() => setTab("counter")}>
            Compteur prix
          </button>
          <button type="button" className="tab tab-user" onClick={handleChangeUser}>
            Changer d'utilisateur
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
            onReset={resetPrize}
            showPopup={showPrizePopup}
            onClosePopup={closePrizePopup}
          />
        )}
      </main>

      {showPrizePopup && tab !== "counter" && (
        <div className="popup-overlay" role="dialog" aria-modal="true" aria-label="Félicitations">
          <div className="popup-card">
            <p>🎉</p>
            <h3>Félicitations {currentUser}, tu as gagné le grand prix !</h3>
            <button type="button" onClick={closePrizePopup}>
              Super !
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
