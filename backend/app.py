from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import re
import json

app = Flask(__name__)
CORS(app)

# ----------------------------
# Data Loading and Preprocessing
# ----------------------------
# Load and preprocess constitutional data.
# (Ensure your CSV has columns: 'article', 'title', 'description')
constitution_df = pd.read_csv('constitution_of_india.csv')
constitution_df['text'] = constitution_df['title'] + ': ' + constitution_df['description']
constitution_df = constitution_df.rename(columns={'article': 'article_no'})

# ----------------------------
# Model Setup for Constitutional Analysis
# ----------------------------
# Using a lightweight SentenceTransformer model.
model = SentenceTransformer('all-MiniLM-L6-v2')
article_texts = constitution_df['text'].tolist()
article_embeddings = model.encode(article_texts, convert_to_tensor=True)

# Threshold for constitutional relevance.
SIMILARITY_THRESHOLD = 0.4

# ----------------------------
# Fallback Model Setup for General Legal Reasoning
# ----------------------------
# Use a local text-to-text generation model as a fallback.
fallback_generator = pipeline("text2text-generation", model="google/flan-t5-base")

# ----------------------------
# Helper Functions for Constitutional Analysis
# ----------------------------

def find_relevant_articles(query, threshold=SIMILARITY_THRESHOLD, top_k=3):
    """
    Find constitutional articles relevant to the query using cosine similarity.
    If no article exceeds the threshold, return an empty list.
    """
    query_embedding = model.encode([query], convert_to_tensor=True)
    similarities = cosine_similarity(
        query_embedding.cpu().numpy(),
        article_embeddings.cpu().numpy()
    )[0]
    
    if similarities.max() < threshold:
        return []
    
    sorted_indices = np.argsort(-similarities)
    top_indices = [idx for idx in sorted_indices if similarities[idx] >= threshold][:top_k]
    
    relevant_articles = []
    for idx in top_indices:
        article = constitution_df.iloc[idx].to_dict()
        article['similarity'] = float(similarities[idx])
        relevant_articles.append(article)
    return relevant_articles

def generate_analysis(query, articles):
    """
    Generate a legal analysis summary based on the most relevant constitutional articles.
    """
    if not articles:
        return ("No clear constitutional precedent was found for this query. "
                "It is possible that the issue does not fall under constitutional provisions.")
    
    main_article = articles[0]
    main_topic = main_article.get('title', 'Unknown Topic').split(':')[0].strip().lower()
    key_principle = main_article.get('description', '').split('.')[0].strip()
    
    analysis = (f"Legal analysis of this situation primarily relates to {main_topic}. "
                f"Article {main_article.get('article_no', 'N/A')} states: {key_principle.capitalize()}.")
    
    if len(articles) > 1:
        supplementary = articles[1]
        supplementary_principle = supplementary.get('description', '').split('.')[0].strip()
        analysis += (f" Supplementary context from Article {supplementary.get('article_no', 'N/A')}: "
                     f"{supplementary_principle.lower()}.")
    return analysis

def determine_verdict(articles):
    """
    Determine a verdict (YES/NO/MAYBE) based on the language in the constitutional articles.
    Uses simple keyword matching.
    """
    if not articles:
        return "MAYBE"
    
    # Check for exceptions (e.g., medicinal usage).
    for article in articles:
        text = article.get('text', '').lower()
        if re.search(r'except\s+for\s+medicinal\s+purposes', text):
            return "YES"
    
    # Check for prohibitive language.
    prohibited_terms = [r'\bprohibit\b', r'\billegal\b', r'\bforbid\b', r'\bban\b']
    for article in articles:
        text = article.get('text', '').lower()
        if any(re.search(term, text) for term in prohibited_terms):
            return "NO"
    
    # Check for permissive language.
    permitted_terms = [r'\bright\b', r'\bpermit\b', r'\ballow\b', r'\blegal\b']
    for article in articles:
        text = article.get('text', '').lower()
        if any(re.search(term, text) for term in permitted_terms):
            return "YES"
    
    return "MAYBE"

# ----------------------------
# Fallback Legal Reasoning via Local Model
# ----------------------------

def analyze_query_with_fallback(query):
    """
    Use a local text-to-text generation model to analyze the legal query.
    The prompt instructs the model to act as a legal expert.
    It must provide:
      - A verdict (YES, NO, or MAYBE)
      - A constitutional or statutory basis if applicable (or "None")
      - Detailed judicial reasoning.
    If the query is absurd (for example, marrying a tree), the response should explain that
    non-human entities cannot legally consent and the act is not legally valid (verdict NO).
    Return ONLY a valid JSON object with the keys: 'verdict', 'constitutional_basis', and 'judicial_reasoning'.
    """
    prompt = (
        "You are a legal expert. Analyze the following legal query. "
        "Determine its legality and provide a verdict of YES, NO, or MAYBE. "
        "If applicable, cite any constitutional or statutory basis, otherwise state 'None'. "
        "Provide detailed judicial reasoning. "
        "If the query is absurd or not legally recognized (for example, marrying a tree), "
        "explain that non-human entities cannot legally consent and the act is not legally valid, yielding a verdict of NO. "
        "Return ONLY a valid JSON object with exactly three keys: 'verdict', 'constitutional_basis', and 'judicial_reasoning'.\n\n"
        f"Query: {query}\n"
    )
    
    result = fallback_generator(prompt, max_length=512, do_sample=True, temperature=0.6)
    generated_text = result[0]['generated_text']
    
    # Try to extract a JSON object from the generated text.
    json_match = re.search(r'(\{.*\})', generated_text, re.DOTALL)
    if json_match:
        json_text = json_match.group(1)
        try:
            result_json = json.loads(json_text)
            return result_json
        except Exception as e:
            pass  # We'll fall back to heuristic parsing.
    
    # Heuristic: if the output is very short (like "No" or "Yes"), map it.
    simple_output = generated_text.strip().lower().rstrip('.')
    if simple_output in ["no", "yes", "maybe"]:
        if simple_output == "no":
            return {
                "verdict": "NO",
                "constitutional_basis": "None",
                "judicial_reasoning": (
                    "Marriage requires legal capacity and the ability to provide consent. "
                    "Since non-human entities, such as trees, cannot provide legal consent, "
                    "such a union is not legally recognized."
                )
            }
        elif simple_output == "yes":
            return {
                "verdict": "YES",
                "constitutional_basis": "None",
                "judicial_reasoning": (
                    "While this is an unconventional query, the answer 'Yes' suggests a legal recognition. "
                    "However, in practical legal terms, marriage is defined as a union between consenting humans. "
                    "Thus, this result may be spurious."
                )
            }
        else:  # maybe
            return {
                "verdict": "MAYBE",
                "constitutional_basis": "None",
                "judicial_reasoning": "The query is unconventional and does not clearly fall under standard legal provisions."
            }
    
    # If we still cannot parse valid JSON, return a fallback message.
    return {
        "verdict": "MAYBE",
        "constitutional_basis": "None",
        "judicial_reasoning": f"Failed to parse JSON from generated text. Full text: {generated_text}"
    }

# ----------------------------
# API Endpoint
# ----------------------------

@app.route('/analyze', methods=['POST'])
def analyze_situation():
    try:
        data = request.json
        situation = data.get('situation', '').strip()
        if not situation:
            return jsonify({
                'verdict': "MAYBE",
                'articles': [],
                'reasoning': "Please provide a situation to analyze."
            })
        
        # First, attempt constitutional analysis.
        relevant_articles = find_relevant_articles(situation)
        if relevant_articles:
            verdict = determine_verdict(relevant_articles)
            analysis = generate_analysis(situation, relevant_articles)
            clean_articles = [{k: v for k, v in article.items() if k != 'similarity'} 
                              for article in relevant_articles]
            response = {
                'verdict': verdict,
                'articles': clean_articles,
                'reasoning': analysis
            }
        else:
            # Fallback: use the local model for general legal reasoning.
            llm_result = analyze_query_with_fallback(situation)
            response = {
                'verdict': llm_result.get('verdict', 'MAYBE'),
                'articles': [{
                    'article_no': '',
                    'title': 'Not applicable',
                    'description': llm_result.get('constitutional_basis', 'None')
                }],
                'reasoning': llm_result.get('judicial_reasoning', '')
            }
        
        return jsonify(response)
        
    except Exception as e:
        app.logger.error(f"Error during analysis: {str(e)}")
        return jsonify({
            'verdict': "MAYBE",
            'articles': [],
            'reasoning': f"Analysis error: {str(e)}"
        }), 500

# ----------------------------
# Run the App
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
