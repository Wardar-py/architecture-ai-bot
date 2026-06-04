## Реализация RAG-бота с техниками промптинга

### 1. Архитектура и выбор компонентов

Для бота использован следующий стек:
- **Векторное хранилище**: ChromaDB.
- **Эмбеддинги**: `sentence-transformers/all-MiniLM-L6-v2`.
- **LLM**: `llama3.1:8b`.
- **Интерфейс**: консольный REPL (цикл вопрос-ответ).

Пайплайн реализован на базе LangChain с кастомной цепочкой, чтобы внедрить Few-shot и Chain-of-Thought.

### 2. Результаты
[результат_1](https://github.com/Wardar-py/architecture-ai-bot/blob/rag/task4/1.png)
[результат_2](https://github.com/Wardar-py/architecture-ai-bot/blob/rag/task4/2.png)
[результат_3](https://github.com/Wardar-py/architecture-ai-bot/blob/rag/task4/3.png)
[результат_4](https://github.com/Wardar-py/architecture-ai-bot/blob/rag/task4/4.png)
[результат_5](https://github.com/Wardar-py/architecture-ai-bot/blob/rag/task4/5.png)
 

