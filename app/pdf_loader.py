from langchain_community.document_loaders import PyPDFLoader

def extract_text(pdf_path):
    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    text = ""

    for doc in documents:
        text += doc.page_content + "\n"

    return text