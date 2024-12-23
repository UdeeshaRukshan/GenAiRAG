from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

# Initialize Chroma client
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="growing_vegetables")

# Load PDF documents
loader = PyPDFDirectoryLoader(DATA_PATH)
raw_documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)
chunks = text_splitter.split_documents(raw_documents)

# Prepare lists for upsert
documents = []
metadata = []
ids = []

for i, chunk in enumerate(chunks):
    if chunk.page_content.strip():  # Ensure content is not empty
        documents.append(chunk.page_content)
        ids.append(f"ID{i}")
        metadata.append(chunk.metadata)

# Check if lists are non-empty before upsert
if not documents or not metadata or not ids:
    raise ValueError("Documents, metadata, or IDs list is empty. Check input data.")

# Upsert into the collection
collection.upsert(
    documents=documents,
    metadatas=metadata,
    ids=ids
)
