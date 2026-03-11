## Context

This is a greenfield homelab project. There is no existing codebase — only a `knoledgebase/` directory containing exam question documents (PDF, DOCX, ODT) organized by professor name (malusa, messetti, zoccante). The study group needs a self-hosted quiz app served via Docker. Students access it from phones and laptops on the local network (or via reverse proxy).

## Goals / Non-Goals

**Goals:**
- Extract structured multiple-choice questions from heterogeneous source documents
- Serve a fast, mobile-friendly quiz experience with no login or server-side state
- Make it trivially deployable on a homelab with `docker compose up`
- Keep the architecture simple enough that a non-frontend-specialist can maintain it

**Non-Goals:**
- User accounts, authentication, or progress tracking
- Real-time multiplayer or leaderboards
- Runtime LLM calls — all AI work happens offline in the extraction step
- Editing questions through the webapp UI
- Supporting languages other than Italian

## Decisions

### 1. Static SPA over full-stack framework
**Choice**: Svelte + Vite producing a static build served by nginx.
**Rationale**: The app is stateless (no login, no persistence). A full-stack framework (Next.js, SvelteKit SSR) adds a Node.js runtime in production for zero benefit. Static files + nginx is simpler to deploy, faster to serve, and has a smaller attack surface.
**Alternatives considered**:
- Next.js / SvelteKit with SSR: Unnecessary runtime complexity for a stateless app
- Plain HTML/JS (no framework): Viable but manual DOM management gets messy for quiz interactivity
- React + Vite: Would work, but more boilerplate for a small app; Svelte is leaner

### 2. Questions as static JSON files (not a database)
**Choice**: One JSON file per exam in a `data/` directory, bundled into the static build.
**Rationale**: No writes happen at runtime. JSON files are easy to inspect, version control, and regenerate. SQLite would add complexity for read-only data that fits in a few KB per exam.
**Alternatives considered**:
- SQLite served via API: Overkill — no queries beyond "load all questions for exam X"
- Embedded in JS bundle: Harder to update independently of the app code

### 3. GitHub Copilot LLM for extraction (user-selectable model)
**Choice**: Use the GitHub Copilot API (GitHub Models) from the extraction script, allowing the user to choose which model to use.
**Rationale**: The user already has a GitHub Copilot subscription. This avoids a separate OpenAI/Anthropic API key and billing. The OpenAI-compatible endpoint at GitHub Models makes integration straightforward with the standard OpenAI Python SDK.
**Alternatives considered**:
- Direct OpenAI API: Requires separate API key and billing
- Local LLM (Ollama): Quality may be insufficient for generating plausible Italian-language distractors
- Manual extraction: Too time-consuming for the volume of documents

### 4. Offline extraction pipeline (not runtime AI)
**Choice**: Run the extraction script once per batch of new documents. Output is committed JSON.
**Rationale**: No runtime dependency on an LLM API. The webapp works fully offline after build. Extraction results can be reviewed and corrected before serving.
**Alternatives considered**:
- Runtime LLM calls per quiz session: Expensive, slow, requires API availability

### 5. Client-side shuffling
**Choice**: Shuffle question order and alternative order in the browser at quiz start using Fisher-Yates.
**Rationale**: Trivial to implement, no server needed. JSON stores canonical order with correct answer index; the app remaps after shuffle.

## Risks / Trade-offs

- **[PDF parsing quality]** → Some PDFs may be scanned images rather than text. Mitigation: Use `pymupdf` which has OCR fallback; flag documents that produce low-confidence text for manual review.
- **[Generated distractors quality]** → LLM-generated wrong answers may be obviously wrong or accidentally correct. Mitigation: Output JSON is reviewed by a human before serving. The extraction script can flag questions where it generated alternatives.
- **[Italian language specificity]** → LLM may produce grammatically awkward Italian distractors. Mitigation: Use a high-quality model (GPT-4o or Claude) and Italian-language prompts.
- **[No progress tracking]** → Students can't see which topics they're weak on. Mitigation: Accepted trade-off for simplicity. Can be added later with localStorage if needed.
