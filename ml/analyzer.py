from transformers import pipeline
import torch

# Load model once
@st.cache_resource
def load_model():
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

def analyze_text(text):
    """Analyze journal text for depression risk"""
    
    model = load_model()
    
    # Get sentiment
    result = model(text[:512])[0]  # Truncate to model limit
    
    # Simple risk calculation (improve with better model)
    score = 1 - result['score'] if result['label'] == 'NEGATIVE' else result['score'] * 0.3
    
    # Classify risk level
    if score < 0.33:
        risk_level = "Low"
    elif score < 0.67:
        risk_level = "Moderate"
    else:
        risk_level = "High"
    
    return {
        'score': score,
        'risk_level': risk_level,
        'sentiment': result['label']
    }