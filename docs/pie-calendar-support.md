# Pie Calendar support model

This folder now contains a trained Jeffy model named `csrouter`, a static answer
catalog, per-label confidence thresholds, and a local support CLI. It classifies
English questions and retrieves a prewritten answer; no LLM or external API is
called during inference. The English encoder is already cached.

## Try it

From `/Users/elijahmills/Documents/csrouter`:

```sh
./csrouter ask "How do I create recurring events?"
./csrouter ask "How do I add VAT information to my invoice?"
./csrouter ask "How can I show a Google Calendar ICS feed?"
./csrouter ask "Please refund my purchase"
./csrouter ask "My license won't authenticate and the plugin update says unauthorized"
./csrouter ask "How do I enable dark mode?" --json
./csrouter chat
./csrouter labels
```

An automatic answer includes its documentation links. JSON output also includes
the model's label, final route, confidence, threshold, margin, review status,
and handoff state. Licensing problems can select `license_activation`, whose
product-owner-approved response refers the customer to support@piecalendar.com.
Its `response_type` is `support_referral` and its handoff records an email method
and `mailto:` URL, ready for a future redirect or handoff integration. This is a
specific referral, not a claim to have fixed or activated a customer's license.
Policy-triggered human requests can skip classification, in
which case the predicted label is null and the final route is `human_required`.

Chat can request up to two new clarification messages. It never automatically
repeats an unchanged query. Explicit human requests and investigation requests
go directly to the human route. Type `/quit` to exit.

The human message is the requested fallback text. The result also links to
Pie Calendar's contact page and reports `submitted: false`: this experiment
does **not** email support or send a conversation anywhere. A real handoff
integration is required before deployment.

To inspect raw classifier output without answer-routing safeguards:

```sh
HF_HUB_OFFLINE=1 ./jeffy predict csrouter \
  "How do I create recurring events?" --pack-dir models/jeffy
```

## What was prepared

- 63 public documentation articles were snapshotted locally. Source URLs, dates,
  and content hashes are recorded in `data/support/sources.json`; full source
  snapshots stay in the ignored `vendor/jeffy/cache` directory.
- 30 response labels plus `human_required` cover setup, views, upcoming lists,
  language, dark mode, mobile widget mode, title wrapping, end dates, recurrence,
  CPTs, taxonomy filters, builders, blocks, event details, custom date fields,
  colors, popovers, submission forms, CSV import, licensing, invoices, and
  Connector integrations, and licensing support referrals.
- `data/support/train.csv` contains 791 synthetic examples. The original answer
  labels each have 12 unique seed questions plus 12 product-context variants;
  `license_activation` has 16 seeds plus 16 variants, and the human label has
  63 unique policy examples. Augmented variants are not independent customer
  observations.
- `data/support/calibration.csv` contains 104 separately authored questions.
- `data/support/evaluation.csv` contains 154 separately authored questions,
  including 30 questions that should require a human.
- `config/support/routes.json` contains the generated answers, source links,
  threshold settings, enabled flags, and the fallback message.
- The model artifacts are in `models/jeffy/csrouter/`, including training
  provenance and dataset hashes. They are ignored by Git; copy them explicitly
  when packaging the application, or recreate them with `./csrouter train`.

The documentation-based examples and answers are agent-generated drafts. The
`license_activation` contact response was approved directly by the product owner;
the other answers still need product-owner review before customer-facing use.

## Routing policy

1. Application rules immediately escalate requests for humans, refunds, account
   investigation, unresolved errors, current commercial terms, and similar
   matters outside the static answer catalog.
2. License activation/authentication problems bypass only general unresolved-error
   rules so Jeffy can select the approved licensing referral. Refunds, explicit
   human requests, and account interventions retain their normal priority. The
   exception cannot unlock unrelated answers merely by mentioning a license.
3. Jeffy classifies the question using the `csrouter` task.
4. Clearly separate supported intents in one query request clarification.
5. The selected label must have an enabled answer, its confidence must strictly
   exceed its threshold, and its lead over the second-highest probability must
   be at least 0.15.
6. Otherwise the result requires a human; chat may first gather clarification.

Thresholds are selected per label from 0.85, 0.90, 0.925, 0.95, 0.975, and 0.99.
A route needs at least two accepted calibration examples with no observed wrong
answers. Routes without that evidence stay disabled. The training pipeline
compares regularization settings `C=0.01` and `C=0.1` using calibration only,
selecting the one with more error-free automatic answers. It selected `C=0.1`.
No final evaluation results are used to choose `C` or thresholds.

Two routes remain disabled: `add_to_calendar` and `connector_webhooks`.
Their answers and training examples are present, but automatic retrieval needs
more calibration evidence. Requests may therefore receive a human response even
when a relevant documentation answer exists. Never lower thresholds just to
force an answer without examining wrong-answer risk.

Classifier confidence is not a calibrated probability that a support answer is
correct. The explicit escalation rules are conservative heuristics, not a
complete detector for unsupported questions.

## Evaluation and limitations

```sh
./csrouter evaluate
vendor/jeffy/.venv/bin/python -m unittest discover -s tests -v
```

The runtime evaluation uses the frozen model and routing policy, including the
human overrides and multiple-intent check. Its detailed results are saved in
`reports/support/runtime_evaluation.json`. The original training evaluation and
calibration reports are also preserved under `reports/support`.

In the updated evaluation, 91 of 154 questions received an automatic response
(including licensing support referrals), and all 30 human-required questions
were escalated. Of the 91 responses, 90 matched
the exact expected label. One matched a source-checked equivalent answer: the
question asking which block displays single-event information was originally
labeled `block_editor`, while the model selected `event_info`, whose answer
names the correct block. This equivalence is explicitly recorded in
`data/support/evaluation_reviews.json`; exact-label accuracy remains separately
reported rather than relabeling the test or changing the model.

Synthetic examples are useful for experimentation, but they do not establish
real-customer accuracy or a production safety guarantee. The calibration set is
small (three questions per original answer label and five for licensing), and the same agent authored the
training and evaluation examples. Replace/expand evaluation with real support
questions before relying on these thresholds. English-only support, short
queries, unfamiliar wording, and multi-part requests remain limitations.

Source review avoided repeating two questionable statements: the custom-post-
type troubleshooting article's contradictory `exclude_from_search` wording,
and the CSV-import article's malformed sample date. The answers refer to the
relevant settings/meta reference without repeating those questionable details.

## Review and improve

1. Read `docs/support-answer-review.md` and edit `config/support/routes.json`.
   Confirm each answer against the live documentation and actual supported
   product versions. Changing answer wording alone does not require retraining.
2. Add reviewed real questions to `data/support/train.csv`. Label according to
   the answer they should receive. Keep unsupported and investigation requests
   in `human_required`.
3. Add separately reviewed questions to the calibration CSV. Keep conversation
   families and near-duplicate templates together, not across splits.
4. Maintain a separate evaluation set. Do not tune thresholds from final-test
   failures; use fresh final-test questions after making repeated improvements.
5. Retrain and evaluate:

   ```sh
   ./csrouter train
   ./csrouter evaluate
   ```

6. Review the detailed accepted/rejected examples, not just overall accuracy.
   Product-owner approval should gate a production release of model and answers.

`./csrouter train` recalibrates and overwrites the active local model and
thresholds. Save an existing version first if you want to compare or roll back.
`scripts/prepare_support_data.py` recreates the synthetic seed and overwrites
the CSVs and routing configuration; do not rerun it after editing your reviewed
data unless that reset is intentional. `scripts/fetch_pie_docs.py` prepares
source snapshots and uses a persistent HTML cache; clear that cache deliberately
when you want a fresh documentation snapshot.

## Minimal architecture

`csrouter` → local Python environment → escalation rules → Jeffy classifier →
threshold/margin check → static JSON answer or human-required state.

The added routing/data scripts use the Python standard library and Jeffy's
already-installed dependencies. No new packages were installed. Hosting,
tenant isolation, widgets, support-system integration, and a production review
workflow remain future application work.
