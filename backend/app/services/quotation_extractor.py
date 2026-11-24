
from io import BytesIO
from pathlib import Path

import fitz  # PyMuPDF
from openpyxl import load_workbook


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def extract_pdf(file_bytes: bytes) -> dict:
    """Extract text from a PDF quotation."""

    text_parts = []

    with fitz.open(stream=file_bytes, filetype="pdf") as document:
        for page_number, page in enumerate(document, start=1):
            page_text = page.get_text("text")
            if page_text.strip():
                text_parts.append(
                    f"--- Page {page_number} ---\n{page_text}"
                )

    extracted_text = "\n\n".join(text_parts)

    if not extracted_text.strip():
        return {
            "text": "",
            "warning": "No selectable text found. This may be a scanned PDF and requires OCR."
        }

    return {
        "text": extracted_text,
        "warning": None
    }


def extract_excel(file_bytes: bytes) -> dict:
    """Extract cell contents from an Excel quotation."""

    workbook = load_workbook(
        BytesIO(file_bytes),
        read_only=True,
        data_only=True
    )

    sheets = []

    for worksheet in workbook.worksheets:
        rows = []

        for row in worksheet.iter_rows(values_only=True):
            values = [
                str(value).strip()
                for value in row
                if value is not None
            ]

            if values:
                rows.append(" | ".join(values))

        if rows:
            sheets.append(
                f"--- Sheet: {worksheet.title} ---\n"
                + "\n".join(rows)
            )

    workbook.close()

    extracted_text = "\n\n".join(sheets)

    if not extracted_text.strip():
        raise ValueError("The Excel file contains no readable data.")

    return {
        "text": extracted_text,
        "warning": None
    }


def extract_quotation(file_bytes: bytes, filename: str) -> dict:
    """Validate and extract a supported quotation document."""

    if not file_bytes:
        raise ValueError("Uploaded file is empty.")

    if len(file_bytes) > MAX_FILE_SIZE:
        raise ValueError("File size must not exceed 10 MB.")

    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        result = extract_pdf(file_bytes)
        file_type = "pdf"

    elif extension == ".xlsx":
        result = extract_excel(file_bytes)
        file_type = "xlsx"

    else:
        raise ValueError(
            "Unsupported file format. Upload a PDF or XLSX file."
        )

    return {
        "filename": Path(filename).name,
        "file_type": file_type,
        "text": result["text"],
        "warning": result["warning"]
    }
