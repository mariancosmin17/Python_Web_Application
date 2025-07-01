from flask import request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

model_name = "clapAI/modernBERT-base-multilingual-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def analyze_sentiment_ro():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Textul este necesar"}), 400

    result = sentiment_pipeline(text)[0]
    return jsonify({
        "text": text,
        "sentiment": result["label"],
        "score": result["score"]
    }), 200
