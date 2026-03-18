#!/usr/bin/env python3
"""
kela-quiz extraction pipeline.

Reads source documents (PDF, DOCX, ODT, PNG) from knoledgebase/<professor>/,
uses a GitHub Copilot LLM to extract and structure multiple-choice questions,
and writes one JSON file per professor to the output directory.

The output JSON is always deleted and fully regenerated on each run.

Usage:
    # With copilot-api proxy (default):
    #   1. Start proxy:  npx copilot-api@latest start
    #   2. Run extraction:
    python extract.py --professor all --output-dir ../data
    python extract.py --professor malusa --model claude-sonnet-4.6 --output-dir ../data
    python extract.py --professor malusa --model gpt-5.1 --output-dir ../data

    # With GitHub Models API (GPT-4o only, no Claude/GPT-5):
    python extract.py --base-url https://models.inference.ai.azure.com --model gpt-4o --professor all

Environment:
    GITHUB_TOKEN  Your GitHub personal access token with Copilot access
"""

import argparse
import base64
import json
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the same directory as this script
load_dotenv(Path(__file__).parent / ".env")

import fitz  # pymupdf
import jsonschema
from docx import Document as DocxDocument
from odf import text as odf_text
from odf.opendocument import load as odf_load
from openai import OpenAI

# ─── Schema ──────────────────────────────────────────────────────────────────

QUESTION_SCHEMA = {
    "type": "object",
    "required": ["id", "question", "alternatives", "correct", "generated"],
    "properties": {
        "id": {"type": "integer"},
        "question": {"type": "string", "minLength": 1},
        "alternatives": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2,
            "maxItems": 4,
        },
        "correct": {"type": "integer", "minimum": 0, "maximum": 3},
        "generated": {"type": "boolean"},
    },
    "additionalProperties": False,
}

OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["professor", "questions"],
    "properties": {
        "professor": {"type": "string"},
        "questions": {"type": "array", "items": QUESTION_SCHEMA},
    },
}

# ─── Prompt loading ───────────────────────────────────────────────────────────

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(name: str) -> str:
    """Load a prompt from a .md file in the prompts directory."""
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8").strip()


# ─── Image helpers ────────────────────────────────────────────────────────────

IMAGE_SYSTEM_PROMPT = load_prompt("image_system")


MAX_IMAGE_PIXELS = 1920  # longest side — keeps quality while staying under API limits


def image_to_base64(path: Path) -> tuple[str, str]:
    """Load, downscale if needed, and return (base64_str, mime_type)."""
    from PIL import Image
    import io

    img = Image.open(path)
    if max(img.size) > MAX_IMAGE_PIXELS:
        img.thumbnail((MAX_IMAGE_PIXELS, MAX_IMAGE_PIXELS), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    mime = "image/png"
    return base64.b64encode(buf.getvalue()).decode("utf-8"), mime


def extract_questions_from_image(
    path: Path, client: OpenAI, model: str
) -> list[dict]:
    """Send a PNG screenshot to the vision LLM and parse the structured questions."""
    b64, mime = image_to_base64(path)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": IMAGE_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{b64}", "detail": "high"},
                    },
                    {
                        "type": "text",
                        "text": load_prompt("image_user"),
                    },
                ],
            },
        ],
        temperature=0.1,
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        questions = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  ⚠ JSON parse error for {path.name}: {e}", file=sys.stderr)
        print(f"  Raw response:\n{raw[:500]}", file=sys.stderr)
        return []

    if not isinstance(questions, list):
        print(f"  ⚠ Expected list for {path.name}", file=sys.stderr)
        return []

    return questions


# ─── Text extraction ──────────────────────────────────────────────────────────

def extract_text_pdf(path: Path) -> str:
    """Extract text from a PDF file using pymupdf."""
    doc = fitz.open(str(path))
    pages = [page.get_text() for page in doc]
    doc.close()
    return "\n".join(pages)


def extract_text_docx(path: Path) -> str:
    """Extract text from a DOCX file using python-docx."""
    doc = DocxDocument(str(path))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_text_odt(path: Path) -> str:
    """Extract text from an ODT file using odfpy."""
    doc = odf_load(str(path))
    paragraphs = doc.getElementsByType(odf_text.P)
    lines = []
    for p in paragraphs:
        text = ""
        for node in p.childNodes:
            if hasattr(node, "data"):
                text += node.data
        if text.strip():
            lines.append(text)
    return "\n".join(lines)


def extract_text(path: Path) -> str:
    """Dispatch to the correct extractor based on file extension."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_text_pdf(path)
    elif suffix == ".docx":
        return extract_text_docx(path)
    elif suffix == ".odt":
        return extract_text_odt(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")


# ─── LLM extraction ──────────────────────────────────────────────────────────

SYSTEM_PROMPT = load_prompt("text_system")


def extract_questions_with_llm(
    text: str, client: OpenAI, model: str, professor: str, source_file: str
) -> list[dict]:
    """Send extracted text to the LLM and parse the structured questions."""
    user_prompt = load_prompt("text_user").format(
        professor=professor, source_file=source_file, text=text
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        questions = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  ⚠ JSON parse error for {source_file}: {e}", file=sys.stderr)
        print(f"  Raw response:\n{raw[:500]}", file=sys.stderr)
        return []

    if not isinstance(questions, list):
        print(f"  ⚠ Expected list, got {type(questions)} for {source_file}", file=sys.stderr)
        return []

    return questions


# ─── Validation ──────────────────────────────────────────────────────────────

def validate_question(q: dict, idx: int) -> dict | None:
    """Validate and normalise a single question dict. Returns None if invalid."""
    try:
        jsonschema.validate(q, QUESTION_SCHEMA)
        return q
    except jsonschema.ValidationError as e:
        print(f"  ⚠ Question {idx} failed validation: {e.message}", file=sys.stderr)
        return None


def validate_output(data: dict) -> None:
    jsonschema.validate(data, OUTPUT_SCHEMA)


# ─── Aggregation ─────────────────────────────────────────────────────────────

def process_professor(
    professor: str,
    knoledgebase_dir: Path,
    output_dir: Path,
    client: OpenAI,
    model: str,
) -> int:
    """Process all documents and images for a professor. Returns number of questions extracted."""
    prof_dir = knoledgebase_dir / professor
    if not prof_dir.is_dir():
        print(f"⚠ Directory not found: {prof_dir}", file=sys.stderr)
        return 0

    text_extensions = {".pdf", ".docx", ".odt"}
    image_extensions = {".png", ".jpg", ".jpeg", ".webp"}

    text_files = [f for f in prof_dir.iterdir() if f.suffix.lower() in text_extensions]
    image_files = [f for f in prof_dir.iterdir() if f.suffix.lower() in image_extensions]

    if not text_files and not image_files:
        print(f"⚠ No supported files found in {prof_dir}", file=sys.stderr)
        return 0

    # Always start fresh — delete any existing output
    out_path = output_dir / f"{professor}.json"
    if out_path.exists():
        out_path.unlink()
        print(f"  🗑  Deleted existing {out_path.name}")

    print(f"\n📚 Processing professor: {professor} ({len(text_files)} document(s), {len(image_files)} image(s))")

    all_questions = []
    q_id = 1

    for f in sorted(text_files):
        print(f"  📄 Extracting text from: {f.name}")
        try:
            text = extract_text(f)
        except Exception as e:
            print(f"  ⚠ Failed to extract text from {f.name}: {e}", file=sys.stderr)
            continue

        if not text.strip():
            print(f"  ⚠ No text found in {f.name}", file=sys.stderr)
            continue

        print(f"  🤖 Sending to LLM ({model})...")
        raw_questions = extract_questions_with_llm(text, client, model, professor, f.name)

        valid = 0
        for q in raw_questions:
            q["id"] = q_id
            validated = validate_question(q, q_id)
            if validated:
                all_questions.append(validated)
                q_id += 1
                valid += 1

        print(f"  ✓ Extracted {valid} valid questions from {f.name}")

    seen_questions = {q["question"].strip().lower() for q in all_questions}

    for f in sorted(image_files):
        print(f"  🖼  Processing image: {f.name}")
        raw_questions = extract_questions_from_image(f, client, model)

        valid = 0
        for q in raw_questions:
            key = q["question"].strip().lower()
            if key in seen_questions:
                print(f"  ↩  Skipping duplicate: {q['question'][:60]}...")
                continue
            seen_questions.add(key)
            q["id"] = q_id
            validated = validate_question(q, q_id)
            if validated:
                all_questions.append(validated)
                q_id += 1
                valid += 1

        print(f"  ✓ Extracted {valid} valid questions from {f.name}")

    output_data = {"professor": professor, "questions": all_questions}

    try:
        validate_output(output_data)
    except jsonschema.ValidationError as e:
        print(f"⚠ Output validation failed for {professor}: {e.message}", file=sys.stderr)

    out_path = output_dir / f"{professor}.json"
    out_path.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  💾 Saved {len(all_questions)} questions → {out_path}")

    # Report generated alternatives
    generated = [q for q in all_questions if q.get("generated")]
    if generated:
        print(f"  ⚠ {len(generated)} question(s) have AI-generated alternatives — review recommended:")
        for q in generated:
            print(f"     • [{q['id']}] {q['question'][:80]}...")

    return len(all_questions)


# ─── CLI ─────────────────────────────────────────────────────────────────────

KNOWN_PROFESSORS = ["malusa", "messetti", "zoccante"]


def main():
    parser = argparse.ArgumentParser(
        description="Extract quiz questions from source documents using a GitHub Copilot LLM."
    )
    parser.add_argument(
        "--professor",
        default="all",
        help='Professor name (e.g. "malusa") or "all" to process all. Default: all',
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help='Model to use (e.g. gpt-4o, claude-sonnet-4.5, gpt-5.1). Default: gpt-4o',
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:4141/v1",
        help='API base URL. Default: http://localhost:4141/v1 (copilot-api proxy). '
             'Start the proxy with: npx copilot-api@latest start',
    )
    parser.add_argument(
        "--output-dir",
        default="../data",
        help='Output directory for JSON files. Default: ../data',
    )
    parser.add_argument(
        "--knoledgebase-dir",
        default="../knoledgebase",
        help='Path to knoledgebase directory. Default: ../knoledgebase',
    )
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN environment variable not set.", file=sys.stderr)
        print("   Set it to your GitHub personal access token with Copilot access.", file=sys.stderr)
        sys.exit(1)

    import urllib.request
    import urllib.error

    proxy_url = args.base_url
    if "localhost" in proxy_url or "127.0.0.1" in proxy_url:
        try:
            urllib.request.urlopen(proxy_url.rstrip("/").rsplit("/", 1)[0] + "/", timeout=2)
        except Exception:
            print("❌ Cannot reach the copilot-api proxy at:", proxy_url, file=sys.stderr)
            print("   Start it with:  npx copilot-api@latest start", file=sys.stderr)
            sys.exit(1)

    client = OpenAI(
        base_url=args.base_url,
        api_key=token,
    )

    knoledgebase_dir = Path(args.knoledgebase_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.professor == "all":
        professors = KNOWN_PROFESSORS
    else:
        professors = [args.professor]

    total = 0
    for prof in professors:
        total += process_professor(prof, knoledgebase_dir, output_dir, client, args.model)

    print(f"\n✅ Done! Total questions extracted: {total}")


if __name__ == "__main__":
    main()
