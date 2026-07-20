# Allocator Token Risk Harness

A risk-weighted token-efficiency harness by **Katrina Li**. It routes each request between local and frontier models according to confidence, entropy, expected cost, and reliability requirements.

The harness first asks a local model whether a request is safe for local handling. When that probe passes, it generates a short local answer with log probabilities enabled and measures token entropy plus top-1 confidence. High-confidence work stays local; uncertain or high-risk work escalates to any OpenAI-compatible remote endpoint.

## Why it exists

- Reduce frontier-token consumption without applying one model to every task.
- Keep low-risk, high-confidence requests on local infrastructure.
- Escalate uncertain work when reliability matters more than marginal cost.
- Produce visible routing traces for evaluation and tuning.
- Support capacity-aware local inference and a configurable remote fallback.

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
