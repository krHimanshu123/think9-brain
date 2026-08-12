from pathlib import Path
from typing import Any
import re

BRAND_LABELS = ["Brand Alpha", "Brand Beta", "Brand Gamma", "Portfolio"]

def infer_brand(filename: str) -> str:
    name = filename.lower()
    for key, label in (("alpha", "Brand Alpha"), ("beta", "Brand Beta"), ("gamma", "Brand Gamma")):
        if key in name:
            return label
    return "Portfolio"

def infer_category(filename: str) -> str:
    name = filename.lower()
    mapping = {"research": "Consumer Research", "meeting": "Meeting", "performance": "Growth Experiment", "growth": "Growth Experiment", "supply": "Supply Chain", "packaging": "Product Strategy", "playbook": "SOP / Playbook", "strategy": "Product Strategy"}
    return next((value for key, value in mapping.items() if key in name), "Product Strategy")

def load_documents(data_dir: str | Path) -> list[dict[str, Any]]:
    docs = []
    for path in sorted(Path(data_dir).glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        docs.append({"id": path.name, "name": path.name, "title": path.stem.replace("_", " ").title(), "brand": infer_brand(path.name), "category": infer_category(path.name), "date": "2026-02-18", "type": "Internal knowledge", "text": text, "indexed": True})
    return docs

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()

def extract_upload(uploaded_file: Any) -> str:
    if uploaded_file.name.lower().endswith(".txt"):
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    from pypdf import PdfReader
    import io
    reader = PdfReader(io.BytesIO(uploaded_file.getvalue()))
    return "\n".join(page.extract_text() or "" for page in reader.pages)
