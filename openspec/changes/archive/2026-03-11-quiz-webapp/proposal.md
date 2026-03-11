## Why

A study group needs a way to practice for university exams (Malusà, Messetti, Zoccante). Exam questions exist as PDFs, DOCX, and ODT files but there's no interactive way to drill them. Students currently re-read static documents — ineffective for retention. A self-hosted quiz webapp lets the group practice with randomized multiple-choice questions anytime, on any device.

## What Changes

- **New extraction pipeline**: Python script that reads source documents (PDF, DOCX, ODT), extracts questions and correct answers, uses an LLM via GitHub Copilot (user chooses which model) to structure them as multiple-choice (generating plausible wrong alternatives where only the correct answer exists), and outputs one JSON file per exam.
- **New quiz webapp**: Svelte + Vite single-page application where students select an exam, choose how many questions they want, and take a randomized quiz with immediate per-question feedback and a final score.
- **Self-hosted deployment**: Dockerfile and docker-compose.yaml to build and serve the app with nginx.
- Questions are shuffled each session (both question order and alternative order within each question).
- Exams are kept strictly separate — no mixing of questions across professors.

## Capabilities

### New Capabilities
- `question-extraction`: Python pipeline to extract and structure questions from PDF/DOCX/ODT source documents using text extraction libraries and a GitHub Copilot-provided LLM (user-selectable model), outputting validated JSON per exam.
- `quiz-ui`: Svelte SPA with exam selection, configurable quiz length, randomized question/alternative order, per-question feedback, and final score display. Mobile-friendly, no login required.
- `deployment`: Dockerfile (multi-stage: build Svelte app, serve with nginx) and docker-compose.yaml for self-hosted deployment.

### Modified Capabilities
<!-- None — this is a greenfield project. -->

## Impact

- **New dependencies**: Node.js/npm (Svelte + Vite), Python 3 (extraction script), GitHub Copilot account (LLM access for extraction)
- **New files**: `extraction/` directory, `data/` directory (JSON output), `app/` directory (Svelte app), `Dockerfile`, `docker-compose.yaml`
- **Infrastructure**: Requires Docker on the homelab server to deploy
- **Source documents**: Read-only — the extraction pipeline reads from `knoledgebase/` but does not modify them
