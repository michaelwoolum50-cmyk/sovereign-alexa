# Friction Log

## 1. MCP spec — SSE stream semantics for simple request/response
- **Attempted:** implement GET `/mcp` SSE per spec 2025-11-25.
- **Expected:** clear guidance on minimal viable stream for demos.
- **Happened:** spec describes the full bidirectional lifecycle; the minimal
  "POST in, JSON out" path that 90% of demos need is buried.
- **Severity:** moderate. **Workaround:** implemented a courtesy SSE hello-event
  stream; primary path is plain POST JSON-RPC. **Suggestion:** publish a
  "minimal server" reference implementation alongside the spec.

## 2. Devpost — prize total inconsistency
- **Attempted:** confirm the prize pool for the submission writeup.
- **Expected:** one number.
- **Happened:** page header says "$138,000 in prizes"; body says "$190K value of
  cash and AWS credits."
- **Severity:** minor. **Workaround:** cited both with context. **Suggestion:**
  single source of truth for the prize figure.

## 3. RemoteOK API — tag coverage varies
- **Attempted:** pull gig leads across six tags.
- **Expected:** consistent results per tag.
- **Happened:** some tags return empty on a given day; `data-entry` is reliable.
- **Severity:** low. **Workaround:** default tag + graceful empty handling.
  **Suggestion:** n/a (third-party API, not Amazon's).
