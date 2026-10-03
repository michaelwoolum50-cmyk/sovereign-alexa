# Sovereign for Alexa+ — Your Agentic Workforce, by Voice

**Track:** Alexa+ (simulated agentic experience) · **Mini challenges:** Open Source, AWS Builder-ready

## What it is

Sovereign turns Alexa+ into the front door of a personal AI workforce. Speak naturally —
*"find me paying gigs I can do today"* — and a local orchestrator decomposes the request,
fans it out to specialist agents running **in parallel**, screens every result against
hard rails, and speaks back a synthesized answer. Everything runs on your own hardware:
a local open-source LLM does the thinking, a self-hosted MCP server does the doing.

No cloud bill. No data leaving your house. Your workforce, your rules.

## How it works

```
Voice/text ──▶ Alexa+ ──▶ Sovereign MCP server (spec 2025-11-25, Streamable HTTP)
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
        gig_finder        gig_screener       app_tracker
     (live RemoteOK    (never-pay rails:   (pipeline build
      public API)      hard-pass paywalls)   status)
              └─────────────────┼─────────────────┘
                                ▼
                    synthesized spoken answer
```

The `orchestrate` tool does the fan-out with real threads — 2–3 specialists,
~3 seconds, every result screened before it reaches you.

## The never-pay rails

Sovereign refuses to waste your time on listings that want your money first.
Any gig requiring a deposit, minimum balance, or subscription to bid/apply is
hard-rejected automatically — "they want a penny, it's a hard pass." Scam
markers (crypto payment pushes, off-platform contact demands) are rejected too.

## Run it

```bash
# 1. Start the MCP server (stdlib only — no dependencies)
python3 mcp_server.py            # → 127.0.0.1:8787

# 2. Open the simulated Alexa+ experience
open web/index.html              # or serve: python3 -m http.server 8080 --directory web
```

Ask it: *"find me paying gigs"*, *"how are my apps doing?"*, *"find me work and check my apps"*.

## MCP tools

| Tool | What it does |
|------|--------------|
| `find_gigs` | Live leads from RemoteOK's public API (attribution honored, links back to source) |
| `screen_gig` | Applies the never-pay / scam rails → PASS or REJECT with reason |
| `app_status` | Reads the autonomous app-pipeline build state |
| `orchestrate` | Decomposes a request, runs specialists in parallel, synthesizes |

Verified live: `initialize` → `tools/list` → `tools/call` round-trips clean;
`orchestrate("find me paying gigs")` returned 5 real screened gigs in 2.9s.

## Why this matters

Job platforms gate opportunity behind paywalls; AI assistants gate capability
behind cloud subscriptions. Sovereign removes both gates: a voice interface anyone
can use, powered by an agent workforce that runs on a home computer and refuses
to let its owner be scammed. The pattern generalizes — every revenue stream gets
its own local agent swarm, orchestrated the same way.

## Built during the hackathon window

All code in this repo was written for this submission (Oct 3–23, 2026), on top of
the author's pre-existing local agent-orchestration patterns. The MCP server, web
experience, rails, and demo are new.

## License

MIT — see LICENSE. Built in the open.
