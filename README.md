# EventMind
AI-агент для ивент-маркетинга: pipeline + tool use + semantic search

Демо-проект AI-интеграции: автономный агент который за 30 секунд 
генерирует полный маркетинг-пакет для любого события.

## Что умеет агент

- Semantic search — находит похожие референсы по смыслу
- Tool use — ищет актуальные тренды в интернете в реальном времени
- Pipeline — цепочка из 3+ шагов где каждый шаг использует результат предыдущего
- Structured output — возвращает данные в JSON формате
- Готовый UI на Gradio

## Что генерирует

- Концепцию и название события
- Контент-план для Instagram (3 поста)
- Email-приглашение для гостей
- Чеклист подготовки
- Хэштеги

## Технологии

- Python
- Groq API (LLM)
- Sentence Transformers (embeddings)
- DuckDuckGo Search (tool use)
- Gradio (UI)

## Как запустить

1. Установи зависимости: `pip install groq sentence-transformers duckduckgo-search gradio`
2. Добавь Groq API ключ в код
3. Запусти: `python app.py`
