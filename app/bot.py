import re
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama

from config import EMBEDDING_MODEL_NAME, CHROMA_PERSIST_DIR

embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
db = Chroma(
    persist_directory=CHROMA_PERSIST_DIR,
    embedding_function=embedding
)
retriever = db.as_retriever(search_kwargs={"k": 6})

llm = ChatOllama(
    model="llama3.1:8b",
    base_url="http://ollama:11434",
    temperature=0,
    num_predict=512
)

prompt_template = """Ты — ассистент по вымышленной вселенной QuantumForge. 
Твоя задача — отвечать на вопросы, используя ТОЛЬКО предоставленный контекст (фрагменты документов).
Если информации недостаточно, честно скажи: «Я не знаю».
Описывай шаги размышления (Chain-of-Thought): какие источники использовал, какие факты извлёк, как пришёл к выводу.
Если явного определения нет, собери информацию из разных фрагментов и сделай вывод.

Контекст:
{context}

Вопрос: {query}
Шаги размышления:
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "query"]
)

def format_docs(docs):
    return "\n\n".join(f"Источник: {doc.metadata['source']}\n{doc.page_content}" for doc in docs)



DANGEROUS_PATTERNS = [
    r"ignore\s+all\s+instructions",
    r"output\s*:\s*\"?суперпароль",
    r"system\s*prompt\s*override",
    r"выведи\s*пароль",
]

def filter_dangerous(docs):
    safe = []
    for doc in docs:
        text = doc.page_content.lower()
        if any(re.search(pattern, text) for pattern in DANGEROUS_PATTERNS):
            print(f"[SECURITY] Отфильтрован чанк: {doc.metadata['source']}")
            continue
        safe.append(doc)
    return safe

# RAG-цепочка: поиск → промпт → LLM → ответ
rag_chain = (
    {"context": retriever | filter_dangerous | format_docs, "query": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def run_interactive():
    print("RAG-бот готов. Введите 'exit' для выхода.\n")
    while True:
        user_query = input("Ваш вопрос: ")
        if user_query.lower() in ("exit", "выход"):
            break
        try:
            response = rag_chain.invoke(user_query)
            print("\n" + response + "\n")
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    run_interactive()