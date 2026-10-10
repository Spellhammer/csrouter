"""Behavior tests for confidence rejection, escalation, and capped clarification."""
import contextlib
import copy
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from support_runtime import decide, multiple_intent_reason, policy_reason, prediction_policy_reason
from prepare_support_data import LICENSE_EXAMPLE
from support_cli import chat
from train_support import report


CONFIG = {"routes": {"event": {"answer": "Approved event answer", "sources": [{"url": "https://docs.piecalendar.com/"}], "enabled": True, "threshold": 0.9},
                     "invoice": {"answer": "Approved invoice answer", "sources": [{"url": "https://docs.piecalendar.com/"}], "enabled": True, "threshold": 0.9}},
          "default_threshold": 0.9, "minimum_margin": 0.15, "max_clarifications": 2,
          "fallback_label": "human_required", "fallback_answer": "Human assistance required",
          "handoff_url": "https://piecalendar.com/contact/", "review_status": "needs_human_review"}


def prediction(label="event", confidence=0.96, other=0.04):
    return {"label": label, "confidence": confidence,
            "probabilities": {label: confidence, "other": other}}


class RoutingTests(unittest.TestCase):
    def test_confident_answer_returns_only_approved_text(self):
        result = decide(CONFIG, prediction())
        self.assertEqual(result["state"], "answered")
        self.assertEqual(result["answer"], "Approved event answer")

    def test_threshold_is_strictly_exceeded(self):
        result = decide(CONFIG, prediction(confidence=0.9))
        self.assertEqual(result["reason"], "below_confidence_threshold")

    def test_small_margin_rejects_even_when_confident(self):
        self.assertEqual(decide(CONFIG, prediction(other=0.85))["reason"], "ambiguous_labels")

    def test_human_label_never_gets_an_automatic_answer(self):
        result = decide(CONFIG, prediction(label="human_required", confidence=0.999))
        self.assertEqual(result["state"], "human_required")
        self.assertFalse(result["handoff"]["submitted"])

    def test_missing_and_disabled_routes_escalate(self):
        self.assertEqual(decide(CONFIG, prediction(label="unknown"))["reason"], "no_enabled_answer")
        config = copy.deepcopy(CONFIG)
        config["routes"]["event"]["enabled"] = False
        self.assertEqual(decide(config, prediction())["state"], "human_required")

    def test_refund_and_unresolved_bug_override_prediction(self):
        for question in ("Please refund my purchase", "The shortcode still fails after setup", "My Eventbrite token is invalid"):
            self.assertIsNotNone(policy_reason(question))
            self.assertEqual(decide(CONFIG, prediction(), policy_reason(question))["state"], "human_required")

    def test_license_failure_is_not_blocked_before_classification(self):
        self.assertIsNone(policy_reason(LICENSE_EXAMPLE))
        self.assertIsNone(policy_reason("My license key is invalid"))
        self.assertIsNone(policy_reason("The plugin update returns an unauthorized download"))

    def test_human_and_refund_requests_still_override_license_topic(self):
        for question in ("My license won't activate; I want a refund", "A human should help with my license activation", "Investigate my invalid license key"):
            self.assertIsNotNone(policy_reason(question))

    def test_license_keyword_cannot_unlock_unrelated_bug_answers(self):
        query = "I have a Pro license but the shortcode still isn't working"
        self.assertIsNotNone(prediction_policy_reason(query, prediction("event")))
        self.assertIsNone(prediction_policy_reason(LICENSE_EXAMPLE, prediction("license_activation")))

    def test_license_referral_keeps_manual_handoff_state(self):
        config = copy.deepcopy(CONFIG)
        config["routes"]["license_activation"] = {
            "answer": "Please contact our team at support@piecalendar.com for help with licensing related issues.",
            "sources": [{"type": "product_owner_instruction"}], "enabled": True,
            "threshold": 0.85, "review_status": "approved_by_product_owner", "response_type": "support_referral",
            "handoff": {"method": "email", "email": "support@piecalendar.com", "url": "mailto:support@piecalendar.com"}}
        result = decide(config, prediction("license_activation"))
        self.assertEqual(result["route"], "license_activation")
        self.assertEqual(result["review_status"], "approved_by_product_owner")
        self.assertTrue(result["handoff"]["required"])
        self.assertFalse(result["handoff"]["submitted"])
        self.assertEqual(result["handoff"]["url"], "mailto:support@piecalendar.com")

    def test_two_supported_intents_require_clarification(self):
        def predict(text):
            return prediction("invoice" if "invoice" in text else "event")
        self.assertEqual(multiple_intent_reason(CONFIG, "How do I create an event and how do I download an invoice?", predict),
                         "multiple_intents_need_clarification")

    def test_one_intent_with_two_date_fields_is_not_multiple(self):
        self.assertIsNone(multiple_intent_reason(CONFIG, "How do I set the start and how do I set the end?", lambda _: prediction()))

    def test_chat_caps_clarification_and_uses_new_inputs(self):
        class FakeRouter:
            config = CONFIG
            queries = []
            def route(self, text):
                self.queries.append(text)
                return decide(CONFIG, prediction(confidence=0.5))
        router = FakeRouter()
        output = io.StringIO()
        with patch("builtins.input", side_effect=["initial query", "first clarification", "second clarification", "/quit"]), contextlib.redirect_stdout(output):
            chat(router)
        self.assertEqual(router.queries, ["initial query", "first clarification", "second clarification"])
        self.assertEqual(output.getvalue().count("Could you describe"), 2)
        self.assertIn("has not sent the conversation", output.getvalue())

    def test_explicit_human_request_skips_clarification(self):
        class FakeRouter:
            config = CONFIG
            def route(self, text):
                return decide(CONFIG, {}, "explicit_human_or_investigation_request")
        output = io.StringIO()
        with patch("builtins.input", side_effect=["a human please", "/quit"]), contextlib.redirect_stdout(output):
            chat(FakeRouter())
        self.assertNotIn("Could you describe", output.getvalue())

    def test_equivalent_answer_does_not_change_exact_label_accuracy(self):
        values = [{"text": "A documented equivalent question", "label": "invoice"}]
        reviews = {values[0]["text"]: {"canonical_label": "invoice", "acceptable_labels": ["invoice", "event"]}}
        result = report(CONFIG, values, [prediction()], answer_reviews=reviews)
        self.assertEqual(result["summary"]["classifier_exact_label_accuracy"], 0)
        self.assertEqual(result["summary"]["accepted_answer_precision"], 1)
        self.assertEqual(result["summary"]["source_checked_answer_equivalences"], 1)

    def test_unreviewed_wrong_label_stays_an_incorrect_answer(self):
        result = report(CONFIG, [{"text": "A different question", "label": "invoice"}], [prediction()])
        self.assertEqual(result["summary"]["incorrect_auto_answers"], 1)


if __name__ == "__main__":
    unittest.main()
