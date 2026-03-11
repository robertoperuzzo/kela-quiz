## 1. Project Setup

- [x] 1.1 Initialize the project root with a basic README and `.gitignore` (Node, Python, macOS)
- [x] 1.2 Scaffold the Svelte + Vite app in `app/` using `npm create vite@latest`
- [x] 1.3 Create the `extraction/` directory with a Python `requirements.txt` (`pymupdf`, `python-docx`, `odfpy`, `openai`)
- [x] 1.4 Create the `data/` directory with a placeholder `.gitkeep`

## 2. Extraction Pipeline

- [x] 2.1 Implement text extraction functions for PDF (pymupdf), DOCX (python-docx), and ODT (odfpy) in `extraction/extract.py`
- [x] 2.2 Implement the LLM structuring logic: send extracted text to GitHub Copilot model with a prompt that outputs JSON questions (with `id`, `question`, `alternatives`, `correct`, `generated` fields)
- [x] 2.3 Add CLI argument parsing: `--model` (LLM model name), `--professor` (single professor or all), `--output-dir` (defaults to `data/`)
- [x] 2.4 Implement per-professor aggregation: combine questions from all files in a professor's folder into one `<professor>.json`
- [x] 2.5 Add JSON schema validation for the output files
- [x] 2.6 Run the extraction pipeline against all three knowledge base folders and verify the output JSON files

## 3. Quiz UI — Exam Selection

- [x] 3.1 Create a JSON index (or auto-discover from `data/`) that maps professor keys to human-readable exam names (e.g., `malusa` → `Malusà`)
- [x] 3.2 Build the landing page component: display exam cards/buttons, one per professor
- [x] 3.3 Build the quiz length selector: after picking an exam, let the student choose how many questions (e.g., 10, 20, 30, all)

## 4. Quiz UI — Quiz Flow

- [x] 4.1 Implement question and alternative shuffling (Fisher-Yates) with correct-answer index remapping
- [x] 4.2 Build the question display component: show question text, 4 clickable alternatives
- [x] 4.3 Implement per-question immediate feedback: green highlight for correct, red + green for wrong, with a "Next" button
- [x] 4.4 Implement quiz progression: track current question index, score, and advance through shuffled questions
- [x] 4.5 Build the final score screen: show score (e.g., "18/20"), offer "Retry" and "Back to exams" buttons

## 5. Quiz UI — Responsive Design

- [x] 5.1 Apply mobile-friendly CSS: responsive layout, tappable alternative buttons, readable fonts on small screens
- [x] 5.2 Test on a mobile viewport (< 768px) and verify no horizontal scrolling, all elements usable

## 6. Deployment

- [x] 6.1 Create a multi-stage `Dockerfile`: stage 1 builds the Svelte app (`npm run build`), stage 2 copies `dist/` and `data/` into an nginx image
- [x] 6.2 Create `docker-compose.yaml` exposing the app on port 8080
- [x] 6.3 Build and run the Docker image, verify the webapp is accessible and functional
