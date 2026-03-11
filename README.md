# kela-quiz

A self-hosted multiple-choice quiz webapp for university exam practice.

## Structure

```
kela-quiz/
├── knoledgebase/         # Source documents (PDF, DOCX, ODT) per professor
├── extraction/           # Python pipeline: documents → structured JSON
├── data/                 # Extracted question JSON files (one per exam)
├── app/                  # Svelte + Vite frontend
├── Dockerfile            # Multi-stage build (Svelte → nginx)
└── docker-compose.yaml   # Self-hosted deployment
```

## Quickstart

### 1. Extract questions from source documents

```bash
cd extraction
pip install -r requirements.txt
```

Copy the `.env` file and add your GitHub token:

```bash
cp .env .env  # already exists — just edit it
```

Edit `extraction/.env`:

```
GITHUB_TOKEN=your_token_here
```

Get your token at [github.com/settings/tokens](https://github.com/settings/tokens) — it needs Copilot access.

Then run the extraction:

```bash
python extract.py --professor all --output-dir ../data
```

Optional flags:
- `--professor malusa` — process a single professor instead of all
- `--model gpt-4o` — choose which GitHub Copilot model to use (default: `gpt-4o`)

### 2. Run locally (dev)

```bash
cd app
npm install
npm run dev
```

### 3. Deploy with Docker

```bash
docker compose up -d
```

The app is available at http://localhost:8080

## Adding new material

1. Place new PDF/DOCX/ODT files in `knoledgebase/<professor>/`
2. Re-run the extraction pipeline
3. Rebuild the Docker image: `docker compose up -d --build`
