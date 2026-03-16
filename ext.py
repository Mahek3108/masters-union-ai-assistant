import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


DATA_FOLDER = "manual_data"
VECTOR_DB_PATH = "vector_db_priority"


print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


documents = []

print("Reading course files...")


for file in os.listdir(DATA_FOLDER):

    if file.endswith(".txt"):

        file_path = os.path.join(DATA_FOLDER, file)

        course_name = file.replace(".txt", "")

        loader = TextLoader(file_path, encoding="utf-8")

        docs = loader.load()

        for doc in docs:

            doc.metadata = {
                "course": course_name,
                "source": file
            }

        documents.extend(docs)


print("Total documents loaded:", len(documents))


print("Splitting into chunks...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)


print("Total chunks:", len(chunks))


print("Creating FAISS vector database...")

vector_db = FAISS.from_documents(
    chunks,
    embeddings
)


vector_db.save_local(VECTOR_DB_PATH)

print("Priority Vector DB created successfully!")