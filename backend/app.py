from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import re

app = Flask(__name__)
CORS(app)

# Load and preprocess constitution data
constitution_df = pd.read_csv('constitution_of_india.csv')
constitution_df['text'] = constitution_df['title'] + ': ' + constitution_df['description']
constitution_df = constitution_df.rename(columns={'article': 'article_no'})

# Load lightweight model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Precompute embeddings
article_embeddings = model.encode(constitution_df['text'].tolist(), convert_to_tensor=True)

def find_relevant_articles(query, threshold=0.25):
    query_embedding = model.encode([query], convert_to_tensor=True)
    similarities = cosine_similarity(
        query_embedding.cpu().numpy(),
        article_embeddings.cpu().numpy()
    )[0]
    
    # Get indices with similarity above threshold, sorted descending
    viable_indices = np.argsort(-similarities)
    top_indices = [idx for idx in viable_indices if similarities[idx] >= threshold][:3]
    
    return [
        {**constitution_df.iloc[idx].to_dict(), 'similarity': float(similarities[idx])}
        for idx in top_indices
    ]

def generate_analysis(situation, articles):
    if not articles:
        return "No clear constitutional precedent found."
    
    analysis_template = """Legal analysis of this situation primarily relates to {main_topic}. 
Article {primary_article} states: {key_principle}"""
    
    main_article = articles[0]
    main_topic = main_article['title'].split(':')[0].lower()
    key_principle = main_article['description'].split('.')[0].lower()
    
    analysis = analysis_template.format(
        main_topic=main_topic,
        primary_article=main_article['article_no'],
        key_principle=key_principle.capitalize()
    )
    
    if len(articles) > 1:
        analysis += f"\nSupplementary context from Article {articles[1]['article_no']}: {articles[1]['description'].split('.')[0].lower()}"
    
    return analysis

def determine_verdict(articles):
    if not articles:
        return "MAYBE"
    
    # Check medical exception first using regex
    for article in articles:
        text = article['text'].lower()
        if re.search(r'except\s+for\s+medicinal\s+purposes', text):
            return "YES"
    
    # Check prohibited terms with word boundaries
    prohibited_terms = [r'\bprohibit\b', r'\billegal\b', r'\bforbid\b', r'\bban\b']
    for article in articles:
        text = article['text'].lower()
        if any(re.search(term, text) for term in prohibited_terms):
            return "NO"
    
    # Check permission terms
    permitted_terms = [r'\bright\b', r'\bpermit\b', r'\ballow\b', r'\blegal\b']
    for article in articles:
        text = article['text'].lower()
        if any(re.search(term, text) for term in permitted_terms):
            return "YES"
    
    return "MAYBE"

@app.route('/analyze', methods=['POST'])
def analyze_situation():
    try:
        data = request.json
        situation = data['situation'][:500].strip()
        
        if not situation:
            return jsonify({
                'verdict': "MAYBE",
                'articles': [],
                'reasoning': "Please provide a situation to analyze."
            })
        
        relevant_articles = find_relevant_articles(situation)
        verdict = determine_verdict(relevant_articles)
        analysis = generate_analysis(situation, relevant_articles)
        
        # Remove technical fields from response
        clean_articles = [{k: v for k, v in a.items() if k != 'similarity'} 
                         for a in relevant_articles]
        
        return jsonify({
            'verdict': verdict,
            'articles': clean_articles,
            'reasoning': analysis
        })
        
    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({
            'verdict': "MAYBE",
            'articles': [],
            'reasoning': f"Analysis error: {str(e)}"
        }), 200

if __name__ == '__main__':
    app.run(debug=True)