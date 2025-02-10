from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline, AutoTokenizer, AutoModel
import torch
import re

app = Flask(__name__)
CORS(app)

# Load constitution data with proper preprocessing
constitution_df = pd.read_csv('constitution_of_india.csv')
constitution_df['text'] = constitution_df['title'] + ': ' + constitution_df['description']
constitution_df = constitution_df.rename(columns={'article': 'article_no'})

# Load legal-specific models
legal_bert = AutoModel.from_pretrained("nlpaueb/legal-bert-base-uncased")
tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")

# Initialize text generation pipeline with constraints
text_generator = pipeline(
    'text-generation',
    model='gpt2',
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1,
    pad_token_id=tokenizer.eos_token_id
)

# Precompute legal document embeddings
def get_bert_embeddings(texts):
    inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = legal_bert(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

article_embeddings = get_bert_embeddings(constitution_df['text'].tolist())

def find_relevant_articles(query, threshold=0.3):
    query_embedding = get_bert_embeddings([query])
    similarities = cosine_similarity(query_embedding, article_embeddings)[0]
    
    # Filter by threshold and return sorted results
    relevant_indices = np.where(similarities >= threshold)[0]
    sorted_indices = relevant_indices[np.argsort(-similarities[relevant_indices])]
    
    return constitution_df.iloc[sorted_indices[:3]].to_dict('records')

def generate_analysis(situation, articles):
    articles_text = "\n".join([f"Article {art['article_no']}: {art['text']}" for art in articles])
    
    prompt = f"""Legal Analysis Template:
Situation: {situation}
Relevant Constitutional Provisions:
{articles_text}

Analysis: Based strictly on the provided articles, this situation appears to be"""
    
    response = text_generator(
        prompt,
        max_new_tokens=150,
        temperature=0.7,
        repetition_penalty=1.5,
        num_return_sequences=1,
        truncation=True
    )[0]['generated_text']
    
    # Extract only the analysis portion
    analysis = response.split("Analysis:")[-1].strip()
    analysis = re.sub(r'\b(?:however|but|although).*', '', analysis, flags=re.IGNORECASE)
    return analysis

def determine_verdict(articles):
    prohibited_terms = ["prohibit", "illegal", "forbid", "ban"]
    permitted_terms = ["right", "permit", "allow", "legal"]
    
    for article in articles:
        text = article['text'].lower()
        if any(term in text for term in prohibited_terms):
            return "NO"
        if any(term in text for term in permitted_terms):
            return "YES"
    return "MAYBE"

@app.route('/analyze', methods=['POST'])
def analyze_situation():
    try:
        data = request.json
        situation = data['situation'][:500]  # Limit input length
        
        # Find relevant articles
        relevant_articles = find_relevant_articles(situation)
        if not relevant_articles:
            return jsonify({'error': 'No relevant laws found'}), 404
            
        # Get verdict
        verdict = determine_verdict(relevant_articles)
        
        # Generate analysis
        analysis = generate_analysis(situation, relevant_articles)
        
        return jsonify({
            'verdict': verdict,
            'articles': relevant_articles,
            'reasoning': analysis
        })
        
    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({'error': 'Analysis failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)