import { useEffect } from "react";

const MAX = 100;

type PrizeCounterProps = {
  count: number;
  onReset: () => void;
  showPopup: boolean;
  onClosePopup: () => void;
};

export function PrizeCounter({
  count,
  onReset,
  showPopup,
  onClosePopup,
}: PrizeCounterProps) {
  useEffect(() => {
    if (!showPopup) return;
    const timer = window.setTimeout(onClosePopup, 5000);
    return () => window.clearTimeout(timer);
  }, [showPopup, onClosePopup]);

  const progress = (count / MAX) * 100;

  return (
    <section className="panel counter-panel">
      <h2>Compteur grand prix</h2>
      <p className="counter-help">
        Chaque bonne réponse au quiz fait monter le compteur. À 100, tu gagnes le grand prix !
      </p>

      <div
        className="counter-display"
        aria-label={`Compteur : ${count} sur ${MAX}`}
      >
        <span className="counter-number">{count}</span>
        <span className="counter-max">/ {MAX}</span>
      </div>

      <div className="progress-track" aria-hidden="true">
        <div className="progress-fill" style={{ width: `${progress}%` }} />
      </div>

      <button type="button" className="secondary" onClick={onReset}>
        Remettre à zéro
      </button>

      {showPopup && (
        <div className="popup-overlay" role="dialog" aria-modal="true" aria-label="Felicitations">
          <div className="popup-card">
            <p>🎉</p>
            <h3>Congratulations Camille you won the big Prize</h3>
            <button type="button" onClick={onClosePopup}>
              Super !
            </button>
          </div>
        </div>
      )}
    </section>
  );
}

export { MAX as PRIZE_MAX };
