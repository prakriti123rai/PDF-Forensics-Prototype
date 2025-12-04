# PDF Forensics Prototype

This prototype extracts metadata and text from PDF documents, computes SHA-256 hashes for integrity verification, and produces a structured CSV report for investigative review.

It is designed as a learning tool to understand document forensics workflows:
- Evidence integrity (SHA-256)
- Metadata analysis (title, author, creation date)
- Bulk extraction for triage
- Non-destructive artifact handling
- Structured reporting for investigators

## Usage

1. Place PDF files inside `data/`.
2. Install dependencies:
