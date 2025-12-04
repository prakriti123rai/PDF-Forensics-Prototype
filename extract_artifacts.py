"""
PDF Document Forensics Prototype
--------------------------------
Extracts metadata, computes SHA-256 hash, and extracts text
from PDF files in the ./data directory. Outputs a CSV report.
"""

import os
import hashlib
import csv
from pathlib import Path
from PyPDF2 import PdfReader
from datetime import datetime

DATA_DIR = Path("data")
OUTPUT_CSV = "report.csv"

def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash for file integrity check."""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha.update(chunk)
    return sha.hexdigest()

def extract_pdf_info(pdf_path: Path):
    """Extract metadata and text from PDF."""
    reader = PdfReader(str(pdf_path))
    info = reader.metadata or {}

    text = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text.append(page_text.strip())

    return {
        "filename": pdf_path.name,
        "path": str(pdf_path.resolve()),
        "sha256": compute_sha256(pdf_path),
        "title": info.get("/Title", ""),
        "author": info.get("/Author", ""),
        "creator": info.get("/Creator", ""),
        "producer": info.get("/Producer", ""),
        "created": info.get("/CreationDate", ""),
        "modified": info.get("/ModDate", ""),
        "text_preview": " ".join(text)[:200].replace("\n", " ")
    }

def main():
    pdf_files = sorted(DATA_DIR.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in ./data")
        return

    # Generate report CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "filename", "path", "sha256",
            "title", "author", "creator", "producer",
            "created", "modified", "text_preview"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for pdf in pdf_files:
            print(f"[+] Processing {pdf.name}")
            data = extract_pdf_info(pdf)
            writer.writerow(data)

    print(f"\nReport generated: {OUTPUT_CSV}")
    print(f"Timestamp: {datetime.utcnow().isoformat()} UTC")

if __name__ == "__main__":
    main()
