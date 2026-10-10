"""Local support routing: Jeffy predictions, static answers, and human handoff state."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config/support/routes.json"

# These are application escalation rules, not answers inferred from documentation.
HUMAN_PATTERNS = [
    r"\b(refund|dispute|charged twice|double.charged|chargeback|hacked|vulnerability)\b",
    r"\b(human|real person|support (?:team|representative|agent)|someone from support)\b",
    r"\b(current price|today.?s?.{0,12}price|renewal price|discount|coupon|custom quote)\b",
    r"\b(fatal|stack trace|exception|production server|security issue|bug report)\b",
    r"\b(investigate|recover|restore)\b",
    r"\b(look up|retrieve|check the status|reset.{0,20}(?:activation|limit)|activation count)\b",
    r"\b(?:can.t|cannot).{0,12}\b(?:log in|login)|\b(?:lost access|account email|account password|account.*hacked)\b",
    r"\b(?:cancel.{0,20}(?:subscription|renewal)|change.{0,20}email|take payment|log into my)\b",
    r"\b(?:legal|tax advice|guarantee.{0,30}(?:wcag|accessibility|compliance)|legal assurances)\b",
    r"\b(?:write.{0,20}(?:custom|php|sql)|custom.{0,20}(?:fix|solution|integration|code)|delete all|erase all)\b",
    r"\b(?:ticket reservation|seat (?:limits|reservations)|event capacity|ship next|features.{0,20}next)\b",
]

UNRESOLVED_PATTERNS = [
    r"\b(still|already tried|despite|followed every|nothing.{0,15}helps|didn.t resolve)\b",
    r"\b(broken|isn.t working|doesn.t work|not working|just fails)\b",
    r"\b(?:my |the )?(?:license|key|token|credentials).{0,25}\b(?:invalid|fails|rejected|rejection)\b",
    r"\b(?:failed|rejected|invalid).{0,25}\b(?:token|credentials|activation|license|payment|checkout)\b",
]


def is_license_activation_query(text):
    licensing = re.search(r"\blicen[cs](?:e|ing)\b", text)
    activation = re.search(r"\b(?:activat\w*|authenticat\w*|unauthori[sz]ed|key|validat\w*|invalid|reject\w*|fails|updat\w*|issues|problems)\b", text)
    return bool(licensing and activation) or bool(re.search(r"\bunauthori[sz]ed\s+(?:plugin\s+)?(?:download|update)\b", text))


def load_config():
    config = json.loads(CONFIG_PATH.read_text())
    if config["fallback_label"] in config["routes"]:
        raise ValueError("The human route must never have an automatic answer mapping")
    for label, route in config["routes"].items():
        if not route.get("answer") or not route.get("sources"):
            raise ValueError(f"Missing answer or source attribution for {label}")
    return config


def policy_reason(text):
    text = text.strip().lower()
    if not text or len(text) > 4000:
        return "empty_or_oversized_query"
    if len(text.split()) < 3:
        return "insufficient_detail"
    if any(re.search(pattern, text) for pattern in HUMAN_PATTERNS):
        return "explicit_human_or_investigation_request"
    # Licensing issues have an approved support-referral route. Do not let general
    # "still fails" rules prevent Jeffy from selecting it; explicit human/account
    # intervention requests continue to take priority.
    if not is_license_activation_query(text) and any(re.search(pattern, text) for pattern in UNRESOLVED_PATTERNS):
        return "explicit_human_or_investigation_request"
    return None


def prediction_policy_reason(text, prediction):
    reason = policy_reason(text)
    if reason:
        return reason
    # The exception applies only when Jeffy actually selects the licensing referral.
    # Merely mentioning a license must not unlock other answers for unresolved bugs.
    if prediction.get("label") != "license_activation" and is_license_activation_query(text.lower()) and any(
        re.search(pattern, text.lower()) for pattern in UNRESOLVED_PATTERNS
    ):
        return "explicit_human_or_investigation_request"
    return None


def multiple_intent_reason(config, text, predict):
    clauses = [part.strip() for part in re.split(r"\band\b|\balso\b|[;?]", text, flags=re.I)
               if len(part.split()) >= 3]
    if len(clauses) > 1:
        labels = set()
        for clause in clauses:
            part = predict(clause)
            if part.get("confidence", 0) > 0.7 and part.get("label") in config["routes"]:
                labels.add(part["label"])
        if len(labels) > 1:
            return "multiple_intents_need_clarification"
    return None


def decide(config, prediction, policy=None):
    label = prediction.get("label")
    confidence = prediction.get("confidence", 0.0)
    probabilities = sorted(prediction.get("probabilities", {}).values(), reverse=True)
    margin = probabilities[0] - probabilities[1] if len(probabilities) > 1 else 0.0
    route = config["routes"].get(label)
    threshold = route.get("threshold", config["default_threshold"]) if route else config["default_threshold"]
    reason = policy
    if reason is None:
        if "error" in prediction:
            reason = "classifier_error"
        elif label == config["fallback_label"]:
            reason = "human_required_label"
        elif not route or not route.get("enabled", True):
            reason = "no_enabled_answer"
        elif confidence <= threshold:
            reason = "below_confidence_threshold"
        elif margin < config["minimum_margin"]:
            reason = "ambiguous_labels"
    accepted = reason is None
    handoff = None
    if accepted and route.get("response_type") == "support_referral":
        handoff = {**route["handoff"], "required": True, "submitted": False}
    elif not accepted:
        handoff = {"required": True, "submitted": False, "url": config["handoff_url"]}
    return {"state": "answered" if accepted else "human_required", "label": label,
            "route": label if accepted else config["fallback_label"],
            "confidence": confidence, "threshold": threshold, "margin": round(margin, 4),
            "reason": "accepted" if accepted else reason,
            "answer": route["answer"] if accepted else config["fallback_answer"],
            "sources": route["sources"] if accepted else [],
            "review_status": route.get("review_status", config["review_status"]) if accepted else config["review_status"],
            "response_type": route.get("response_type", "static_answer") if accepted else "human_required",
            "handoff": handoff}


class Router:
    def __init__(self):
        self.config = load_config()
        self.engine = None

    def _predict(self, text):
        if self.engine is None:
            from jeffy.engine import Engine
            self.engine = Engine(pack_dir=str(ROOT / self.config["model_pack"]), device="cpu")
            self.engine.load()
            if self.config["task_id"] not in self.engine.capabilities:
                raise RuntimeError("csrouter model is missing; run ./csrouter train")
        return self.engine.predict(self.config["task_id"], text)

    def route(self, text):
        policy = policy_reason(text)
        if policy:
            return decide(self.config, {}, policy)
        prediction = self._predict(text)
        # Detect clearly separate supported intents instead of choosing only one answer.
        policy = prediction_policy_reason(text, prediction) or multiple_intent_reason(self.config, text, self._predict)
        return decide(self.config, prediction, policy)
