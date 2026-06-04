from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os
import time

from langchain_text_splitters import RecursiveCharacterTextSplitter
BASE_DIR = Path(__file__).resolve().parent

KNOWLEDGE_BASE_PATH = BASE_DIR.parent / "app" / "knowledge_base"
# 1. Загрузка документов
loader = DirectoryLoader(
    str(KNOWLEDGE_BASE_PATH),
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)
documents = loader.load()
print(f"Загружено документов: {len(documents)}")

# 2. Разбиение на чанки
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
)
chunks = splitter.split_documents(documents)
print(f"Получено чанков: {len(chunks)}")

# 3. Загрузка модели эмбеддингов
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

# 4. Создание и сохранение индекса
start_time = time.time()
db = Chroma.from_documents(
    chunks,
    embedding_model,
    persist_directory="./chroma_index"
)
end_time = time.time()

print(f"Индекс Chroma сохранён в 'chroma_index/'")
print(f"Время индексации: {end_time - start_time:.2f} сек.")