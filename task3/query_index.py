from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
db = Chroma(
    persist_directory="./chroma_index",
    embedding_function=embedding_model
)
results = db.similarity_search_with_score("Кто такой Xarn Velgor?", k=3)

for doc, score in results:
    print(f"[Источник: {doc.metadata['source']}] (релевантность: {score:.3f})")
    print(doc.page_content)
    print("---")