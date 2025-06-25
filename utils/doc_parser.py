import os
import fitz  # PyMuPDF
import docx


def parse_file_to_chunks(file_path: str) -> list[str]:
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".txt":
        return parse_txt(file_path)
    elif ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".docx":
        return parse_docx(file_path)
    elif ext == ".md":
        return parse_md(file_path)
    else:
        print(f"[WARNING] Unsupported file type: {file_path}")
        return []


def parse_txt(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return [p.strip() for p in content.split("\n\n") if p.strip()]


def parse_pdf(file_path: str) -> list[str]:
    doc = fitz.open(file_path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def parse_docx(file_path: str) -> list[str]:
    doc = docx.Document(file_path)
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def parse_md(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return [p.strip() for p in content.split("\n\n") if p.strip()]

def parse_file(file_path: str) -> str:
    """Returns the file contents as a single string, joined from parsed chunks."""
    chunks = parse_file_to_chunks(file_path)
    return "\n\n".join(chunks)