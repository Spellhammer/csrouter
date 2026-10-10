"""Evaluate the frozen csrouter model and exact routing policy without tuning it."""
from datetime import datetime, timezone
import json

from support_runtime import ROOT, Router
from train_support import rows, report, evaluation_reviews


def main():
    router = Router()
    values = rows("evaluation")
    predictions = [router._predict(row["text"]) for row in values]
    result = report(router.config, values, predictions, router._predict, evaluation_reviews())
    result["evaluated_at"] = datetime.now(timezone.utc).isoformat()
    result["limitations"] = ["Synthetic examples, not real-customer accuracy.",
                             "Frozen thresholds; this command does not tune the model or routing policy."]
    target = ROOT / "reports/support/runtime_evaluation.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result["summary"], indent=2))
    print(f"Detailed results: {target}")


if __name__ == "__main__":
    main()
