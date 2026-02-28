from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from typing import List


# Extract data from the PDF Files
def load_pdf_file(data):
    loader = DirectoryLoader(data,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents


# Filter the documents with only required data
def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Given a list of document object, return a new list of document objects
    containing only the 'source' in metadata an the original page_content
    """
    minimal_docs = []
    for doc in docs:
        src = doc.metadata.get('source')
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={'source': src}
            )
        )
    return minimal_docs


# Split the data into Text Chunks
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
    )
    text_chunk = text_splitter.split_documents(minimal_docs)
    return text_chunk


# Download the embedding models from Huggingface
def download_embeddings():
    """ 
    Download and retur the HuggingFace embedding model.
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings

embedding = download_embeddings()