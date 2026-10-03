# Devpost Submission Package — Sovereign for Alexa+

## Track
**Alexa+** (simulated agentic experience path)

## Mini challenges
- **Open Source** — repo carries MIT LICENSE; all code written in the hackathon window.
- **AWS Builder** — architecture is AWS-ready (MCP server is stateless HTTP; designed to run on ECS/Lambda + Bedrock for the cloud tier). AWS integration is documented as the scale path, not yet deployed.

## Tagline
Your agentic workforce, by voice — local AI agents that find paying work and run your business, orchestrated through Alexa+.

## Description (paste to Devpost)

**The problem.** Two gates stand between regular people and AI leverage. Job
platforms gate opportunity behind paywalls — "$20 deposit to bid," "$30/month to
apply." AI assistants gate capability behind cloud subscriptions — your data,
your money, their servers.

**Sovereign removes both gates.** Speak naturally — *"find me paying gigs I can
do today"* — and a local orchestrator decomposes your request, fans it out to
specialist agents running in parallel, screens every result against hard
never-pay rails, and speaks back a synthesized answer. The thinking happens on
your own hardware (open-source local LLM); the doing happens through a
self-hosted MCP server (spec 2025-11-25, Streamable HTTP). Zero cloud cost. Zero
data leaving your house.

**How it works.** The `orchestrate` tool breaks a request into subtasks and runs
them on real threads: `gig_finder` pulls live leads from RemoteOK's public API,
`gig_screener` applies the never-pay rails (any listing wanting a penny to apply
is hard-rejected — "they want a penny, it's a hard pass"), `app_tracker` reads
the autonomous app-pipeline status. Verified live: 2 specialists, 5 real
screened gigs, 2.9 seconds.

**The pattern generalizes.** Every revenue stream gets its own local agent swarm
— gigs, apps, bounties — orchestrated the same way. This demo shows the first
two. The architecture is the product: a personal AI workforce with a voice
interface, running on a home computer, that refuses to let its owner be scammed.

**What's new in the window.** The MCP server, the simulated Alexa+ web
experience, the rails engine, and the demo are all written for this hackathon
(Oct 3–23, 2026), building on the author's pre-existing local agent patterns.

## Demo video
`<3 min YouTube/Vimeo link — TO BE RECORDED>`

## Repo
Public GitHub repo URL — TO BE PUSHED (or private + share with testing@devpost.com and: chris-trag, knmeiss, giolaq, anishamalde, mosesroth, emersonsklar)

## Built with
Python (stdlib MCP server), JavaScript (simulated Alexa+ web experience),
Model Context Protocol 2025-11-25 (Streamable HTTP), RemoteOK public API,
local open-source LLM.

## Try it
```bash
python3 mcp_server.py        # MCP server on 127.0.0.1:8787
# open web/index.html, ask: "find me paying gigs"
```

---

## STATUS / NEXT STEPS FOR PARENT
- [x] Working MCP server (verified: initialize/tools/list/tools/call/orchestrate)
- [x] Simulated Alexa+ web experience
- [x] README, LICENSE (MIT), product feedback, friction log
- [ ] Demo video (<3 min) — needs screen recording + voiceover + YouTube upload
- [ ] GitHub repo push (needs github skill / credentials)
- [ ] Devpost submission (needs browser: account, form fill, video link)
- [ ] Optional: AWS tier (Bedrock) for the AWS Builder mini challenge
