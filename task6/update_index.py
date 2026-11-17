import os, json, time, logging
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


KNOWLEDGE_DIR = Path("/app/knowledge_base")
CHROMA_DIR = Path("/app/chroma_index")
STATE_FILE = Path("/app/state/index_state.json")
LOG_FILE = Path("/app/update.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

if STATE_FILE.exists():
    with open(STATE_FILE, "r") as f:
        prev_state = json.load(f)
else:
    prev_state = {}

new_files = []
for filepath in KNOWLEDGE_DIR.glob("*.md"):
    stat = filepath.stat()
    fname = filepath.name
    if fname not in prev_state or prev_state[fname] < stat.st_mtime:
        new_files.append(filepath)

if not new_files:
    logging.info("Нет новых или изменённых документов. Выход.")
    exit(0)

logging.info(f"Найдено {len(new_files)} новых/обновлённых файлов: {[f.name for f in new_files]}")

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
all_chunks = []
for filepath in new_files:
    loader = TextLoader(str(filepath), encoding="utf-8")
    docs = loader.load()
    chunks = splitter.split_documents(docs)
    all_chunks.extend(chunks)

logging.info(f"Создано чанков: {len(all_chunks)}")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

db = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=embedding_model
)
db.add_documents(all_chunks)

logging.info(f"Добавлено {len(all_chunks)} чанков в индекс. Размер коллекции: {db._collection.count()}")

new_state = {}
for filepath in KNOWLEDGE_DIR.glob("*.md"):
    new_state[filepath.name] = filepath.stat().st_mtime
with open(STATE_FILE, "w") as f:
    json.dump(new_state, f)

logging.info("Индекс успешно обновлён.")