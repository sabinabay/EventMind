import os
import json
import numpy as np
from groq import Groq
from duckduckgo_search import DDGS
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import gradio as gr

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
model_emb = SentenceTransformer('all-MiniLM-L6-v2')

события = [
    "джазовый вечер на крыше с живой музыкой",
    "фэшн-показ молодых дизайнеров",
    "техно вечеринка в заброшенном заводе",
    "арт-выставка современных художников",
    "гастрономический фестиваль уличной еды",
    "йога-ретрит на природе",
    "хип-хоп баттл в клубе",
    "кинопоказ под открытым небом"
]
векторы = model_emb.encode(события)

def search_trends(topic):
    with DDGS() as ddgs:
        results = ddgs.text(f"{topic} тренды 2025", max_results=3)
        return "\n".join([r['body'] for r in results])

def agent_interface(topic):
    вектор = model_emb.encode([topic])
    похожесть = cosine_similarity(вектор, векторы)[0]
    топ = np.argsort(похожесть)[::-1][:2]
    референсы = [события[i] for i in топ]
    тренды = search_trends(topic)

    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""Ты AI-агент для ивент-маркетинга.
Событие: {topic}
Референсы: {референсы}
Тренды: {тренды[:500]}

Ответь ТОЛЬКО в JSON:
{{
  "название": "...",
  "концепция": "...",
  "контент_план": ["пост 1", "пост 2", "пост 3"],
  "email": "...",
  "чеклист": ["пункт 1", "пункт 2", "пункт 3"],
  "хэштеги": ["...", "...", "..."]
}}"""
        }]
    )

    текст = r.choices[0].message.content
    if "```" in текст:
        текст = текст.split("```json")[-1].split("```")[0]
    данные = json.loads(текст)

    return (
        f"🎯 {данные['название']}\n\n{данные['концепция']}",
        "\n\n".join(данные["контент_план"]),
        данные["email"],
        "• " + "\n• ".join(данные["чеклист"]),
        " ".join(данные["хэштеги"])
    )

app = gr.Interface(
    fn=agent_interface,
    inputs=gr.Textbox(label="Опиши своё событие"),
    outputs=[
        gr.Textbox(label="🎯 Концепция"),
        gr.Textbox(label="📱 Контент-план"),
        gr.Textbox(label="📧 Email"),
        gr.Textbox(label="✅ Чеклист"),
        gr.Textbox(label="#️⃣ Хэштеги"),
    ],
    title="🎉 EventMind — AI-агент для ивентов"
)

app.launch()
