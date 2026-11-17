from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CHROMA_PERSIST_DIR = str(BASE_DIR.parent / "app" / "chroma_index")
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
KNOWLEDGE_DIR = BASE_DIR.parent / "app" / "knowledge_base"
CHROMA_DIR = BASE_DIR.parent / "app" / "chroma_index"
STATE_FILE = BASE_DIR / "index_state.json"
LOG_FILE = BASE_DIR / "update.log"
