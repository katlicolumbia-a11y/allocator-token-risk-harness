# Allocator Token Risk Harness

**An execution primitive for allocating intelligence according to consequence, by Katrina Li.**

This repository implements one working layer of the architecture developed in Katrina Li's July 2026 paper, **_Allocating Intelligence: Risk-Weighted Harnesses and Portfolio-Level Control for the Agent Economy_**.

The larger thesis is not that model selection needs another router. It is that enterprises operating long-horizon agents need a portfolio-level control plane: a system that allocates compute, money, verification, and autonomy across a digital workforce according to **verified marginal value** and the downstream cost of failure.

## The thesis: put a live price on being wrong

Difficulty and consequence are different quantities. Difficulty helps determine which model may be capable of producing an answer. Consequence — the decision's **blast radius** — measures what the system stands to lose if that answer is wrong.

In the full Allocator.os architecture, each claim, assumption, tool result, and decision is a node in a causal execution graph. Its blast radius is the downstream work it can invalidate. That makes verification an allocation decision:

- High-blast-radius nodes buy stronger inference, independent re-derivation, additional compute, or human review.
- Low-blast-radius nodes use cheaper or local execution, cache reuse, and proportionate checks.
- Failed verification halts only the affected downstream frontier rather than forcing a complete replay.
- Verified outcomes update each agent's budget, permissions, and earned-autonomy level.

The target metric is therefore not dollars per million tokens. It is **cost per verified successful outcome**, penalized by downstream error impact, recovery cost, latency, and human intervention.

## Where this repository fits

This harness is the model-execution actuator inside that broader control plane. It answers a bounded question: **is the local tier sufficiently reliable for this step, or should execution escalate without losing the conversation?**

The current implementation:

- asks a local route probe whether the requested work is safe for local handling;
- samples a local completion with log probabilities;
- measures average and tail token entropy, top-1 probability, and composite confidence;
- keeps the work local only when every configured reliability gate clears;
- escalates uncertain work to any OpenAI-compatible stronger endpoint;
- preserves conversation state across the handoff;
- emits structured route decisions and visible traces for evaluation; and
- supports explicit fail-open behavior when the local decision service is unavailable.

The harness deliberately makes reliability thresholds configurable. In a complete Allocator deployment, an upstream causal ledger would set those thresholds from the step's blast radius, budget, latency requirement, data-egress policy, agent history, and required reliability. A confident answer can still require independent verification when its blast radius is large; uncertainty alone is not a complete risk model.

## Implemented here versus the full control plane

| Implemented in this repository | Broader Allocator.os architecture |
| --- | --- |
| Local suitability probe | Task decomposition and agent mandates |
| Entropy, top-1, and confidence gates | Causal dependency graph and live blast radius |
| Local-to-stronger-tier escalation | Risk-priced verification and human gates |
| Conversation-preserving handoff | Operational halt and selective revalidation |
| Route traces and calibration cases | Per-agent P&L, budgets, permissions, and earned autonomy |
| Configurable reliability thresholds | Portfolio allocation by verified marginal value |

This distinction is intentional: the code here validates a crucial execution mechanism without claiming that a two-tier dispatcher is the entire system described by the paper.

## Why it matters beyond routing

Long-horizon reliability is multiplicative. Even high per-step accuracy can collapse across a workflow with dozens or hundreds of dependent decisions. Running every step on the most expensive model does not solve that structural problem; it raises cost while still treating all errors as equally consequential.

Allocator's design instead treats intelligence like risk capital. The ledger decides where failure would propagate, the harness supplies the appropriate execution tier, verification is concentrated at the dangerous nodes, and outcomes feed back into future allocations. Model routing is a component. **The product thesis is control over a workforce of agents.**

## Setup

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install
```

Start a local `llama.cpp` OpenAI-compatible server on port `8081`:

```bash
llama-server --port 8081 --jinja --logits-all --model /path/to/model.gguf
```

Resolve the model ID and start the risk service:

```bash
export MODEL_ID="$(curl -s http://127.0.0.1:8081/v1/models | jq -r '.data[0].id')"
export LOCAL_ROUTER_MODEL_ID="$MODEL_ID"
export LOCAL_ROUTER_BACKEND_BASE_URL=http://127.0.0.1:8081/v1
python -m local_router.server
```

Configure any OpenAI-compatible frontier endpoint:

```bash
export ROUTER_REMOTE_BASE_URL=https://api.openai.com/v1
export ROUTER_REMOTE_MODEL=your-frontier-model
export ROUTER_REMOTE_API_KEY=your-api-key
export ROUTER_LOCAL_MODEL="$MODEL_ID"
export ROUTER_LOCAL_BASE_URL=http://127.0.0.1:8080/v1

scripts/allocator-router.sh
```

Or run the extension explicitly:

```bash
pi -e /path/to/allocator-token-risk-harness --model allocator-router/risk-weighted
```

Use `/router-use` to switch to the harness and `/router-status` to inspect its active local and remote routes.

## Risk and efficiency controls

```bash
export ROUTER_ENTROPY_THRESHOLD=0.12
export ROUTER_TOP1_THRESHOLD=0.95
export ROUTER_CONFIDENCE_THRESHOLD=0.97
export ROUTER_SHOW_TRACE=1
export ROUTER_AUTO_SELECT=1
export ROUTER_FAIL_OPEN=remote
export LOCAL_ROUTER_ROUTE_PROBE=1
export LOCAL_ROUTER_ROUTE_PROBE_CONFIDENCE_THRESHOLD=0.80
export LOCAL_ROUTER_ROUTE_PROBE_MAX_TOKENS=64
export LOCAL_ROUTER_PROBE_MAX_CONTEXT_CHARS=12000
export LOCAL_ROUTER_PROBE_MAX_MESSAGE_CHARS=4000
```

## Validation

```bash
npm test
npm run eval:mock
```

## Ownership

Maintained by Katrina Li:

- GitHub: <https://github.com/katlicolumbia-a11y>
- GitLab: <https://gitlab.com/katlicolumbia-a11y>
- LinkedIn: <https://www.linkedin.com/in/katrinacolumbia/>

## License

MIT. See `LICENSE`. The original MIT copyright and permission notice are retained as legally required; the rebranded modifications are copyright Katrina Li.
