# Product Feedback — tools used building Sovereign for Alexa+

## MCP (Model Context Protocol), spec 2025-11-25, Streamable HTTP
- **Used for:** the entire agent-tool layer. Every specialist agent is an MCP tool;
  the orchestrator fans out via `tools/call`.
- **What worked:** the JSON-RPC shape is clean; `tools/list` → `tools/call` is a
  genuinely good abstraction for agentic work. Implementing a minimal server in
  stdlib Python took hours, not days.
- **What needs work:** the spec's Streamable HTTP SSE semantics are under-documented
  for the "one POST, one response" case most demos need — I implemented GET SSE
  as a courtesy stream, but plain POST/JSON would cover 90% of builders.
- **Onboarding:** 7/10 — the spec reads well, but a minimal "hello world" server
  example in the docs would cut onboarding time in half.
- **Would I build with it again:** yes — it's the right layer for agent tools.

## Alexa+ simulated-experience path
- **Used for:** the demo front-end (web app simulating the Alexa+ conversation).
- **What worked:** being allowed to simulate instead of requiring device hardware
  is what made this entry possible for an independent builder.
- **What needs work:** clearer guidance on what "simulated" must still demonstrate
  (we show real MCP calls in code + live data, which felt like the right bar).
- **Would I build with it again:** yes.

## RemoteOK public API
- **Used for:** live gig leads in the `find_gigs` tool (attribution honored).
- **What worked:** simple, fast, no key required. Perfect for demos.
- **Would I build with it again:** yes.
