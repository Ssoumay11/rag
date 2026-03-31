import os
from backend.db.faiss_store import add_documents
from backend.utils.chunking import chunk_text
from pypdf import PdfReader

def load_pdf(file_path, source_name):
    reader = PdfReader(file_path)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    chunks = chunk_text(full_text)

    docs = []
    for chunk in chunks:
        docs.append({
            "text": chunk,
            "metadata": {
                "source": source_name,
                "file": os.path.basename(file_path)
            }
        })

    return docs


def main():
    all_docs = []

    # NEC files
    nec_folder = "backend/data/nec"
    for file in os.listdir(nec_folder):
        if file.endswith(".pdf"):
            path = os.path.join(nec_folder, file)
            all_docs.extend(load_pdf(path, "nec"))

    # Wattmonk files
    wattmonk_folder = "backend/data/wattmonk"
    for file in os.listdir(wattmonk_folder):
        if file.endswith(".pdf"):
            path = os.path.join(wattmonk_folder, file)
            all_docs.extend(load_pdf(path, "wattmonk"))

    print(f"Total chunks: {len(all_docs)}")

    add_documents(all_docs)

    print(" FAISS index created successfully!")


if __name__ == "__main__":
    main()