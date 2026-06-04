## Подготовка базы знаний

### 1. Выбор предметной области и замена терминов

В качестве исходной вселенной взят фандом **Star Wars**.  
Выбрано 32 ключевые страницы: персонажи, планеты, технологии, события.  
Чтобы модель не могла отвечать по памяти, все значимые термины заменены на вымышленные с сохранением внутренней логики мира.

**Принципы замены:**
- Имена персонажей заменены на сгенерированные двух-трёхсложные имена (например, «Darth Vader» → «Xarn Velgor»).
- Планеты переименованы с использованием астрономических или мифологических корней.
- Технологии и объекты получили названия из комбинации технических терминов.
- Концепт «Силы» заменён на «Synth Flux» – вымышленную энергию.

Замена выполнена скриптом `replace_terms.py`, который использует словарь из `terms_map.json` и применяет регулярные выражения с учётом регистра и границ слов.

### 2. Словарь замен (terms_map.json)

```json
{
  "Darth Vader": "Xarn Velgor",
  "Anakin Skywalker": "Zalek Tarn",
  "Luke Skywalker": "Ryon Vex",
  "Leia Organa": "Elys Volan",
  "Han Solo": "Jace Korr",
  "Obi-Wan Kenobi": "Torin Mal",
  "Emperor Palpatine": "Lord Nexar",
  "Yoda": "Kith",
  "Chewbacca": "Gorrak",
  "R2-D2": "D4-M1",
  "C-3PO": "L7-P9",
  "Death Star": "Void Core",
  "Star Destroyer": "Nebula Razer",
  "X-wing": "Shadow Dart",
  "TIE Fighter": "Fang Interceptor",
  "Millennium Falcon": "Vortex Runner",
  "The Force": "Synth Flux",
  "Jedi": "Aether Knight",
  "Sith": "Void Warden",
  "Lightsaber": "Flux Blade",
  "Tatooine": "Varkos",
  "Hoth": "Iskara",
  "Endor": "Lunara",
  "Alderaan": "Thalor Prime",
  "Dagobah": "Morthis",
  "Stormtrooper": "Phalanx Soldier",
  "Rebel Alliance": "Free Worlds Coalition",
  "Galactic Empire": "Nexar Dominion",
  "Wookiee": "Gorrak",
  "Ewok": "Lunari",
  "Hyperdrive": "Void Shifter",
  "Droid": "Automaton",
  "Blaster": "Pulse Rifle"
}
```
### 3. Скрипт замены терминов

Скрипт replace_terms.py читает все .txt файлы из папки raw/, применяет словарь замен, сохраняет результат в knowledge_base/ и параллельно формирует terms_map.json с логом замен.
**Логика работы:**
- Сначала обрабатываются длинные фразы (например, «Darth Vader» до «Vader»).
- Используется re.escape для экранирования специальных символов.
- Флаг re.IGNORECASE гарантирует замену всех форм написания.


### Проверка нераспознаваемости

Проведён поиск в интернете и через ChatGPT (без контекста) фраз «Xarn Velgor», «Void Core», «Synth Flux». Ни один из терминов не дал релевантных результатов, кроме ссылок на сгенерированные самим собой документы.
Таким образом, база полностью изолирована от предварительных знаний модели и подходит для тестирования RAG-пайплайна.