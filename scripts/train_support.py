"""Train csrouter and select routing thresholds using calibration questions only."""
import argparse
import csv
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from support_runtime import CONFIG_PATH, ROOT, decide, prediction_policy_reason, multiple_intent_reason


def rows(name):
    with (ROOT / f"data/support/{name}.csv").open() as file:
        return list(csv.DictReader(file))


def validate_splits(splits, labels):
    seen = {}
    for name, values in splits.items():
        for row in values:
            key = " ".join(row["text"].casefold().split())
            if key in seen:
                raise ValueError(f"Duplicate question in {name} and {seen[key]}")
            seen[key] = name
            if row["label"] not in labels:
                raise ValueError(f"Unknown label {row['label']}")
    if {r["label"] for r in splits["train"]} != set(labels):
        raise ValueError("Every route needs training examples")


def predictions(classifier, values):
    embeddings = classifier.encoder.encode([row["text"] for row in values], batch_size=32,
                                           show_progress_bar=True)
    probs = classifier.clf.predict_proba(classifier.scaler.transform(embeddings))
    classes = classifier.clf.classes_
    results = []
    for row in probs:
        best = int(row.argmax())
        results.append({"label": str(classes[best]), "confidence": round(float(row[best]), 4),
                        "probabilities": {str(label): round(float(p), 4) for label, p in zip(classes, row)}})
    return results


def calibrate(config, values, results):
    """Conservative floor; never tune on final evaluation examples."""
    selected = {}
    for label, route in config["routes"].items():
        candidates = []
        for threshold in [0.85, 0.9, 0.925, 0.95, 0.975, 0.99]:
            config["routes"][label]["threshold"] = threshold
            outcomes = [(row, decide(config, result, prediction_policy_reason(row["text"], result)))
                        for row, result in zip(values, results) if result["label"] == label]
            answered = [row for row, outcome in outcomes if outcome["state"] == "answered"]
            correct = sum(row["label"] == label for row in answered)
            if len(answered) >= 2 and correct == len(answered):
                candidates.append((len(answered), threshold))
        # Leave difficult routes present but disabled when there is too little evidence.
        if candidates:
            count, threshold = sorted(candidates, key=lambda item: (-item[0], item[1]))[0]
            route.update(threshold=threshold, enabled=True)
            selected[label] = {"threshold": threshold, "accepted": count, "observed_errors": 0}
        else:
            route.update(threshold=0.99, enabled=False)
            selected[label] = {"threshold": 0.99, "accepted": 0, "enabled": False,
                               "reason": "fewer_than_two_error_free_calibration_acceptances"}
    return selected


def evaluation_reviews():
    path = ROOT / "data/support/evaluation_reviews.json"
    if not path.exists():
        return {}
    return {review["text"]: review for review in json.loads(path.read_text())["reviews"]}


def report(config, values, results, predict_clause=None, answer_reviews=None):
    records = []
    for row, prediction in zip(values, results):
        policy = prediction_policy_reason(row["text"], prediction)
        if policy is None and predict_clause is not None:
            policy = multiple_intent_reason(config, row["text"], predict_clause)
        result = decide(config, prediction, policy)
        review = (answer_reviews or {}).get(row["text"])
        acceptable = review["acceptable_labels"] if review else [row["label"]]
        if review and (review["canonical_label"] != row["label"] or row["label"] not in acceptable):
            raise ValueError("Evaluation equivalence does not match the canonical label")
        records.append({"text": row["text"], "expected_label": row["label"],
                        "predicted_label": prediction["label"], "confidence": prediction["confidence"],
                        "state": result["state"], "reason": result["reason"], "response_type": result["response_type"],
                        "acceptable_labels": acceptable, "answer_equivalence_review": review,
                        "correct_auto_answer": result["state"] == "answered" and prediction["label"] in acceptable})
    accepted = [r for r in records if r["state"] == "answered"]
    human = [r for r in records if r["expected_label"] == config["fallback_label"]]
    summary = {"questions": len(records), "classifier_exact_label_accuracy": sum(r["expected_label"] == r["predicted_label"] for r in records) / len(records),
               "automatic_answers": len(accepted),
               "self_service_answers": sum(r["response_type"] == "static_answer" for r in accepted),
               "licensing_support_referrals": sum(r["response_type"] == "support_referral" for r in accepted),
               "accepted_answer_precision": sum(r["correct_auto_answer"] for r in accepted) / len(accepted) if accepted else None,
               "coverage": len(accepted) / len(records), "incorrect_auto_answers": sum(not r["correct_auto_answer"] for r in accepted),
               "human_required_questions": len(human),
               "human_required_correctly_escalated": sum(r["state"] == "human_required" for r in human),
               "source_checked_answer_equivalences": sum(r["answer_equivalence_review"] is not None for r in records)}
    return {"summary": summary, "records": records}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--C", type=float, default=None,
                        help="Fixed regularization; otherwise compare 0.01 and 0.1 using calibration only")
    args = parser.parse_args()
    config = json.loads(CONFIG_PATH.read_text())
    # Recalibration starts from the same policy; prior disabled routes must not bias selection.
    for route in config["routes"].values():
        route["enabled"] = True
    splits = {name: rows(name) for name in ("train", "calibration", "evaluation")}
    validate_splits(splits, [*config["routes"], config["fallback_label"]])
    from jeffy.train import train_classifier
    choices = []
    candidate_reports = []
    for regularization in ([args.C] if args.C is not None else [0.01, 0.1]):
        classifier = train_classifier(texts=[r["text"] for r in splits["train"]],
                                      labels=[r["label"] for r in splits["train"]],
                                      task_id=config["task_id"], C=regularization, test_size=0, cv_folds=0)
        calibration_predictions = predictions(classifier, splits["calibration"])
        candidate_config = copy.deepcopy(config)
        calibration = calibrate(candidate_config, splits["calibration"], calibration_predictions)
        score = report(candidate_config, splits["calibration"], calibration_predictions, classifier.predict)
        candidate_reports.append({"C": regularization, "summary": score["summary"]})
        if score["summary"]["incorrect_auto_answers"]:
            raise ValueError("Calibration policy accepted an incorrect answer")
        choices.append((score["summary"]["automatic_answers"], regularization, classifier,
                        candidate_config, calibration_predictions, calibration))
    _, selected_C, classifier, config, calibration_predictions, calibration = sorted(
        choices, key=lambda item: (-item[0], item[1]))[0]
    model_dir = Path(classifier.save(str(ROOT / config["model_pack"])))
    config["calibration"] = {"method": "per_label_threshold_with_0.85_floor_and_0.15_margin",
                             "data": "data/support/calibration.csv", "minimum_acceptances": 2,
                             "status": "synthetic_only_not_production_validation", "labels": calibration,
                             "candidate_models": candidate_reports, "selected_C": selected_C,
                             "selection_rule": "Most calibration auto-answers with zero observed wrong answers; tie prefers smaller C"}
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n")
    # Metadata reflects actual counts, unlike the upstream custom-save defaults.
    manifest_path = model_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest.update(train_examples=len(splits["train"]))
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    provenance = {"task_id": config["task_id"], "trained_at": datetime.now(timezone.utc).isoformat(),
                  "C": selected_C, "train_examples": len(splits["train"]), "synthetic": True,
                  "dataset_hashes": {name: hashlib.sha256((ROOT / f"data/support/{name}.csv").read_bytes()).hexdigest() for name in splits},
                  "routes_sha256": hashlib.sha256(CONFIG_PATH.read_bytes()).hexdigest()}
    (model_dir / "training_provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    reports = ROOT / "reports/support"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "calibration.json").write_text(json.dumps(report(config, splits["calibration"], calibration_predictions, classifier.predict), indent=2) + "\n")
    # Final evaluation uses frozen thresholds. It is not an input to threshold selection.
    evaluation_predictions = predictions(classifier, splits["evaluation"])
    result = report(config, splits["evaluation"], evaluation_predictions, classifier.predict, evaluation_reviews())
    result.update(provenance=provenance, limitations=["Synthetic evaluation, not a real-customer benchmark.",
                                                    "Accepted precision estimates are based on small samples.",
                                                    "Answers still require human product review."])
    (reports / "evaluation.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
