import json
from bot import rag_chain, db

import json
from datetime import datetime

def log_query(query, docs, answer, status):
    record = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "chunks_found": len(docs),
        "answer_length": len(answer),
        "status": status,
        "sources": list(set(d.metadata['source'] for d in docs))
    }
    with open("logs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


with open("golden_questions.json", "r") as f:
    questions = json.load(f)

stats = {"success": 0, "not_found": 0, "error": 0}

for item in questions:
    q = item["question"]
    expected = item["expected"]
    docs = db.similarity_search(q, k=3)
    try:
        answer = rag_chain.invoke(q)
        actual = "success" if len(answer) > 20 and "не знаю" not in answer.lower() else "not_found"
        log_query(q, docs, answer, actual)
        stats[actual] += 1
        print(f"[{actual.upper()}] {q}")
    except Exception as e:
        log_query(q, docs, str(e), "error")
        stats["error"] += 1
        print(f"[ERROR] {q}: {e}")

print("\nРезультаты тестирования:")
print(f"  Успешных ответов: {stats['success']}/{len(questions)}")
print(f"  Отказов (not found): {stats['not_found']}/{len(questions)}")
print(f"  Ошибок: {stats['error']}/{len(questions)}")