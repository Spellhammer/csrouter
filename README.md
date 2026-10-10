# csrouter
Using classifier models with high confidence thresholds to provide actually useful customer support automation.

Jeffy is installed locally in `vendor/jeffy/.venv`. The root `./jeffy`
launcher uses that environment and keeps downloaded encoder models in
`vendor/jeffy/cache/huggingface`. No shell activation is required.

A trained **Pie Calendar support model** is now available:

```sh
./csrouter ask "How do I create recurring events?"
./csrouter chat
./csrouter labels
```

See [the support model guide](docs/pie-calendar-support.md) for training data,
answer review, evaluation results, thresholds, and human-required behavior.
This is a local experiment built from synthetic data; product-owner review is
required before customer-facing deployment.

## Experiment from this folder

```sh
./jeffy --version
./jeffy --help
./jeffy list
./jeffy predict banking77 "I was charged twice for the same transaction"
./jeffy predict sms_spam "WINNER! Reply YES to claim your free cruise."
```

`predict` prints JSON including the winning label, confidence, and probabilities
for the other labels. Specify the classifier explicitly; Jeffy does not choose
a classifier for you. The first text prediction downloads an embedding encoder
(roughly 1.2 GB for the bundled English tasks); subsequent runs use the cache.
Predictions run locally on CPU, without an LLM or API key.
After an encoder is cached, set `HF_HUB_OFFLINE=1` to skip Hugging Face update
checks and run without network access:

```sh
HF_HUB_OFFLINE=1 ./jeffy predict banking77 "I was charged twice"
```

For Jeffy's browser playground:

```sh
./jeffy serve
```

Open <http://localhost:8400>. Stop the server with Ctrl-C.
The launcher binds to localhost by default. Use `./jeffy serve --help` for host,
port, and custom pack options. Server request logs stay in `vendor/jeffy/cache`.

## Train and try your own labels

Start with Jeffy's bundled example:

```sh
./jeffy train --help
./jeffy train --example
./jeffy list --pack-dir models/jeffy
./jeffy predict reviews "The battery life is amazing" --pack-dir models/jeffy
JEFFY_PACK_DIR="$PWD/models/jeffy" ./jeffy serve
```

Training enters an interactive prediction prompt after saving; press Ctrl-C to
exit it. The installed English encoder has already been downloaded and a banking
intent prediction verified, so English experimentation can start immediately.

The launcher defaults training output to `models/jeffy`, separate from the
third-party installation. Override with `--save-dir`. Use your own labeled data:

```sh
./jeffy train --input path/to/training.csv --text-col text --label-col label \
  --task-id support_intents
```

Jeffy supports CSV, TSV, and JSONL. A CSV begins with `text,label` and contains
example questions with the intended label. A custom pack contains your custom
classifiers; it does not automatically merge with the bundled pack.

## Installation and organization

- `jeffy`: project-local CLI launcher.
- `scripts/jeffy_cli.py`: standard-library adapter for list/predict, Jeffy's native training command, and its server.
- `scripts/setup-jeffy.sh`: recreate the environment using pinned packages.
- `vendor/jeffy/requirements.txt`: direct dependency, pinned to `jeffy-classify==0.1.0a14`.
- `vendor/jeffy/requirements.lock.txt`: exact installed dependency versions.
- `vendor/jeffy/.venv/`: third-party code and executables, ignored by Git.
- `vendor/jeffy/cache/`: downloaded models, ignored by Git.
- `models/jeffy/`: your trained models, ignored by Git.

This installation uses Python 3.14.6 on macOS Apple Silicon. Recreate it with
Python 3.14 available (the lock records versions, not platform-specific wheels):

```sh
./scripts/setup-jeffy.sh
```

To use upstream executables or the Python API directly:

```sh
source vendor/jeffy/.venv/bin/activate
export HF_HOME="$PWD/vendor/jeffy/cache/huggingface"
jeffy-train --help
python -c 'from jeffy.engine import Engine; print(Engine)'
deactivate
```

Only Jeffy's required dependencies are installed; its optional build/dev extras
are omitted. Jeffy is currently an alpha release.

## Direction for the final app

Keep reviewed training examples, classifier artifacts, and answer/routing
configuration separate. Start with a versioned JSON routing configuration per
customer, containing a model/task ID, default confidence threshold, optional
per-label thresholds, and a mapping from label to approved answer. Choose
thresholds using held-out examples, including out-of-scope queries; a classifier
score alone does not guarantee that an answer is appropriate.

At runtime, classify the query, apply the configured threshold, and return the
approved answer for the winning label. Keep LLM-assisted labeling and answer
drafting on the training/review side. Human approval should gate publication of
models and answers. Tenant storage and hosted chat/search widgets can follow
once this local workflow is understood.

Repeating an unchanged query with the same model will normally return the same
score. A bounded retry must gather clarification or change its inputs/strategy
to be useful. On exhausted retries, return:

> I'm sorry, I'm not sure I can provide the assistance you're looking for. Let me send this conversation to a human representative and have them help you instead.

The Pie Calendar `csrouter` experiment now implements local routing policy,
answer storage, and capped clarification. Actual human handoff and hosted widgets
remain future application work.

Upstream: [Jeffy documentation](https://github.com/nicobrenner/jeffy)
and [installed PyPI release](https://pypi.org/project/jeffy-classify/0.1.0a14/).
