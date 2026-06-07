"""Add A/B/C/D choices to each question."""
import json
from pathlib import Path
from mcq_choices import add_choices

ROOT = Path(__file__).resolve().parent.parent
IN_PATH = ROOT / "src" / "data" / "questions.json"

if __name__ == "__main__":
    data = json.loads(IN_PATH.read_text(encoding="utf-8"))
    updated = add_choices(data)
    IN_PATH.write_text(json.dumps(updated, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Updated", len(updated), "questions with MCQ choices")
