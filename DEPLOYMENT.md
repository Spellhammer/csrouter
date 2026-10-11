# CSRouter hosting and deployment plan

Documented October 11, 2026. This is the proposed deployment plan, not a record of an existing hosted service.

## Recommended starting deployment

Start with one DigitalOcean Basic Droplet running Ubuntu LTS and Docker Compose. Run a Python routing API behind Caddy, and serve the embeddable widget from the same domain.

Suggested starting size: **4 vCPUs and 8 GiB RAM**. DigitalOcean listed its Regular Basic plan at **$48/month**, excluding backups and taxes, when checked October 10, 2026. Its 2 vCPU / 4 GiB plan was $24/month. Verify pricing before provisioning: [DigitalOcean Droplet pricing](https://www.digitalocean.com/pricing/droplets).

The 8 GiB allocation is a conservative starting point, not a measured requirement. Benchmark memory use and response latency on Linux before launch; downsize if measurements justify it. Start with CPU inference and evaluate whether hardware changes are needed as traffic grows.

DigitalOcean Droplets require us to maintain the operating system, updates, backups, and monitoring. Render is the alternative to consider if managed hosting is more important than direct control: [Render](https://render.com/). Select an always-running service with sufficient memory and an explicit plan for persistent model storage.

## Intended architecture

```text
Customer website
  └─ Embed script inserts search/chat iframe
       └─ Your HTTPS domain
            ├─ Widget assets
            └─ POST /v1/query
                 └─ Resolve customer from widget identifier
                      └─ Jeffy encoder + customer classifier
                           └─ Routing policy and approved answer catalog
                                ├─ Answer
                                ├─ Ask for clarification
                                └─ Human support referral
```

The query is classified against trained labels. The routing policy checks the winning label's confidence threshold, its margin over competing labels, and human-required rules. Accepted labels map to approved, pre-generated answers. Runtime requests do not use an LLM.

For low-confidence requests, ask for new information and classify the clarified query, up to a fixed cap. Repeating an unchanged query does not provide meaningful new evidence. The current CLI allows two clarification messages before falling back to human support.

## Current foundation and remaining work

The project currently provides a local CLI, trained `csrouter` classifier, answer configuration, routing policies, and evaluation tools. The public API, iframe widget, Docker image, and deployment configuration still need to be implemented.

Relevant project files:

- `scripts/support_runtime.py`: routing decisions and human-required policy.
- `config/support/routes.json`: answers, sources, thresholds, and referral configuration.
- `models/jeffy/csrouter/`: trained classifier artifacts.
- `vendor/jeffy/requirements.txt` and `requirements.lock.txt`: local dependency records.
- `docs/pie-calendar-support.md`: training and evaluation guide.
- `docs/support-answer-review.md`: answer review catalog.
- `reports/support/`: calibration and evaluation reports.

Model artifacts and encoder caches are ignored by Git. They must be deliberately included in a deployment release or downloaded through a controlled build/startup process.

## Implementation and deployment steps

### 1. Build the routing API

Use FastAPI and Uvicorn, already included among Jeffy's dependencies. Wrap the existing router in a narrow application API rather than publishing Jeffy's playground/model-management server.

Provide `POST /v1/query` with a request such as:

```json
{
  "widget_id": "pie-calendar-public",
  "query": "My license will not activate"
}
```

Return a documented result containing the outcome, approved answer when applicable, and structured handoff information. Suggested outcomes are `answered`, `clarification_required`, and `human_required`. An answered licensing query can still include a required support referral.

Resolve the widget identifier to trusted server-side customer configuration. The caller must not choose filesystem paths, model files, thresholds, or administrative settings. Refactor the current single-customer configuration loading before supporting multiple customers.

For multi-turn clarification, carry the original question and attempt count in server-managed conversation state or a validated, signed token. Do not trust a browser-supplied attempt count to enforce the cap.

Add liveness and readiness endpoints. Readiness should confirm that the configured model and answer catalog have loaded successfully.

### 2. Package a Linux runtime

Create a Dockerfile that installs pinned, Linux-compatible dependencies and copies the application into the image. Validate dependencies on Linux; do not copy the Mac virtual environment. Use an appropriate CPU-only PyTorch installation for the initial CPU deployment.

Package the trained classifier, answer catalog, and thresholds as one versioned release. Pin the encoder model revision and make its files available before serving requests.

Use persistent Docker volumes for downloaded encoder files and any application data that must survive container replacement. Avoid storing durable data only in a container's writable layer.

### 3. Load and warm up the model

Load the encoder and classifier once during application startup. Run a warm-up prediction before marking the service ready, so the first visitor does not wait for model loading or downloading.

Start with **one Uvicorn worker** and bounded inference concurrency. Separate worker processes can each load another copy of the encoder and multiply RAM usage. Measure latency and resource use before increasing concurrency or worker count.

### 4. Provision the server

Create the selected Ubuntu LTS Droplet in a region close to the initial audience. Install Docker Engine and Compose using the [official Ubuntu installation instructions](https://docs.docker.com/engine/install/ubuntu/).

Configure SSH access, routine system updates, and a firewall. Publish HTTP/HTTPS through Caddy; keep the API container's port internal to the Compose network.

### 5. Configure DNS and HTTPS

Point a subdomain such as `support-api.yourdomain.com` at the server. Run Caddy as the public reverse proxy and serve the API and widget assets through it.

Caddy can provision and renew HTTPS certificates automatically when its prerequisites are met. Preserve its certificate data in a volume: [Caddy automatic HTTPS documentation](https://caddyserver.com/docs/automatic-https).

### 6. Build the embed

Provide a small JavaScript loader that inserts an iframe containing the search or chat interface. Serve the iframe and its API from the same origin to simplify browser integration.

Give each customer a public widget identifier. It identifies an approved public knowledge base; it is not a secret API credential. Administrative APIs require separate authentication.

Add query-size limits, request rate limits, and customer quotas. Enforce customer isolation server-side. If direct cross-origin API access is added later, configure allowed origins explicitly; CORS is not authentication.

### 7. Preserve human routing

Keep explicit human requests and the existing human-required policies ahead of automatic answer selection.

The generic fallback remains:

> I'm sorry, I'm not sure I can provide the assistance you're looking for. Let me send this conversation to a human representative and have them help you instead.

The current implementation supplies a contact link but does **not** submit a conversation or ticket. Until a real integration exists, the widget must make the visitor's next step explicit and must not claim that a handoff was submitted.

The approved `license_activation` answer is:

> Please contact our team at support@piecalendar.com for help with licensing related issues.

Initially, expose the email/contact action. Later, support a customer-configured redirect, ticket system, or human handoff integration, recording whether submission actually succeeded.

### 8. Publish reviewed model releases

Keep training outside the live request process. For the initial deployment, train locally, evaluate the model, review answers, and publish a release containing matching classifier artifacts, answer configuration, and thresholds.

LLMs may help prepare training examples and draft answers; human approval remains part of publication. The deployed runtime uses Jeffy and approved answers only.

Retain the previous release for rollback. Validate a candidate release before switching traffic to it. Avoid overwriting model and answer files independently during active requests.

### 9. Verify and operate the pilot

Before public launch:

- Run the routing tests and evaluation on the packaged Linux runtime.
- Measure warm-up time, resident RAM, and response latency under expected concurrent load.
- Verify clarification limits, low-confidence fallback, explicit human requests, and licensing referrals.
- Verify HTTPS, iframe embedding, request limits, and readiness behavior after a restart.
- Complete human review of the answers intended for publication. Synthetic evaluation scores alone do not establish real-customer accuracy.
- Configure container restart policies, uptime/error monitoring, backups, and a tested restore procedure.

Record release versions, latency, errors, and routing outcomes. If storing visitor queries or conversations, define retention and access controls before enabling those logs.

## Storage plan

For the first Pie Calendar pilot, use versioned model/configuration files and persistent encoder storage. A database is not required just to classify queries and look up static answers.

When customers can manage their own content, add:

- **PostgreSQL** for customers, widget settings, approved answers, thresholds, review state, and model-release references.
- **Object storage** for uploaded documents and versioned model artifacts.
- A separate training job/process for preparing and evaluating candidate releases.

Use the same encoder across compatible customer classifier heads where practical, while keeping each customer's classifier, answers, and configuration isolated. Measure the memory impact as the number of customers grows.

## Scaling plan

Start with one server and one customer. Use measured latency, memory pressure, and traffic to guide the next changes.

First consider more memory or dedicated CPU capacity, bounded queues, and model-loading improvements. For higher availability, move durable data outside the server and run multiple API instances behind a load balancer. Each process or instance still needs enough memory for its loaded models.

The initial deployment does not require Kubernetes or a separate GPU service. Revisit infrastructure as actual usage establishes the requirements.

## Next concrete deliverables

1. A FastAPI wrapper around the existing router, with readiness checks and a documented response contract.
2. A minimal embeddable iframe search/chat widget.
3. A Linux Dockerfile, Docker Compose configuration, and Caddy configuration.
4. A versioned artifact packaging and rollback procedure.
5. Linux resource measurements and a reviewed pilot release.
