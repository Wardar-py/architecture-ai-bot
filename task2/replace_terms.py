import os, json, re

with open("terms_map.json", "r", encoding="utf-8") as f:
    term_map = json.load(f)


sorted_terms = sorted(term_map.items(), key=lambda x: len(x[0]), reverse=True)

def replace_all(text):
    for old, new in sorted_terms:
        pattern = re.compile(re.escape(old), re.IGNORECASE)
        text = pattern.sub(new, text)
    return text

os.makedirs("knowledge_base", exist_ok=True)

for filename in os.listdir("raw"):
    if filename.endswith(".txt"):
        with open(os.path.join("raw", filename), "r", encoding="utf-8") as f:
            raw_text = f.read()
        clean_text = replace_all(raw_text)
        with open(os.path.join("knowledge_base", filename), "w", encoding="utf-8") as f:
            f.write(clean_text)

print("Замена завершена. Файлы сохранены в knowledge_base/")
