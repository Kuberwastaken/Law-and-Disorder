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
constitution_df = pd.read_csv('constitution_of_india.csv')
constitution_df['text'] = constitution_df['title'] + ': ' + constitution_df['description']
constitution_df = constitution_df.rename(columns={'article': 'article_no'})

# ----------------------------
# Model Setup
# ----------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')
article_texts = constitution_df['text'].tolist()
article_embeddings = model.encode(article_texts, convert_to_tensor=True)

# Threshold for constitutional relevance
SIMILARITY_THRESHOLD = 0.4

# Fallback model setup
fallback_generator = pipeline("text2text-generation", model="google/flan-t5-base")

# Extended hardcoded responses for demo questions
DEMO_RESPONSES = {
    "is it legal to marry a tree?": {
        "verdict": "NO",
        "articles": [{
            "article_no": "21; Right to Life and Personal Liberty; Protection of life and personal liberty applies exclusively to persons ",
            "title": "Right to Life and Personal Liberty",
            "description": "Protection of life and personal liberty applies exclusively to persons"
        }, {
            "article_no": "14; Right to Equality; Equality before law and equal protection of laws applies to persons",
            "title": "Right to Equality",
            "description": "Equality before law and equal protection of laws applies to persons"
        }],
        "reasoning": "It isn't legally valid to marry a tree in India. Under Indian law, marriage is a contractual union between two human beings who are capable of giving free and informed consent. Trees, being inanimate objects without legal personhood or the capacity to consent, cannot enter into a marriage contract."
    },
    "can i adopt more than 15 children?": {
        "verdict": "YES",
        "articles": [{
            "article_no": "21; Right to Life and Personal Liberty; Protects an individual's freedom to form a family",
            "title": "Right to Life and Personal Liberty",
            "description": "Protects an individual's freedom to form a family"
        }, {
            "article_no": "14; Right to Equality; Equality before law guarantees freedom of family formation",
            "title": "Right to Equality",
            "description": "Equality before law guarantees freedom of family formation"
        }],
        "reasoning": "The Constitution of India—particularly the right to life and personal liberty under Article 21 and equality before the law under Article 14—protects an individual's freedom to form a family. However, it does not prescribe any numerical limits on family formation or adoption. In other words, no constitutional article imposes a cap."
    },
    "Can I protest with roasts of politicians": {
        "verdict": "YES",
        "articles": [{
            "article_no": "19; Right to Freedom of Speech and Expression; All citizens have the right to assemble peaceably and without arms",
            "title": "Right to Freedom of Speech and Expression",
            "description": "All citizens have the right to assemble peaceably and without arms"
        }],
        "reasoning": "The Constitution of India guarantees the right to peaceful protest under Article 19. Citizens can protest against government policies through peaceful demonstrations, provided they do not violate public order or involve violence."
    },
    "Can my friend sue me if I make fun of him for religion": {
        "verdict": "NO",
        "articles": [{
            "article_no": "15; Prohibition of Discrimination; The State shall not discriminate against any citizen on grounds of religion",
            "title": "Prohibition of Discrimination",
            "description": "The State shall not discriminate against any citizen on grounds of religion, race, caste, sex, or place of birth"
        }, {
            "article_no": "14; Right to Equality; Equality before law and equal protection of laws",
            "title": "Right to Equality",
            "description": "Equality before law and equal protection of laws"
        }],
        "reasoning": "The Constitution explicitly prohibits discrimination based on religion under Article 15. This is further reinforced by Article 14's guarantee of equality before the law. Any form of religious discrimination is unconstitutional."
    },
    "can the government forcefully take my property": {
        "verdict": "MAYBE",
        "articles": [{
            "article_no": "300A ; Right to Property; No person shall be deprived of property save by authority of law",
            "title": "Right to Property",
            "description": "No person shall be deprived of property save by authority of law"
        }],
        "reasoning": "Under Article 300A, the government can acquire private property, but only through legal means and with proper compensation. This is known as eminent domain, but it must be for public purpose and follow due process of law."
    },
    "Can a child work at 12 on their own will": {
        "verdict": "NO",
        "articles": [{
            "article_no": "24; Prohibition of Child Labour; No child below the age of fourteen years shall be employed to work in any factory or mine or engaged in any other hazardous employment",
            "title": "Prohibition of Child Labour",
            "description": "No child below the age of fourteen years shall be employed to work in any factory or mine or engaged in any other hazardous employment"
        }, {
            "article_no": "21A; Right to Education; The State shall provide free and compulsory education to all children aged 6-14 years",
            "title": "Right to Education",
            "description": "The State shall provide free and compulsory education to all children aged 6-14 years"
        }],
        "reasoning": "The Constitution strictly prohibits child labor under Article 24, especially in hazardous conditions. This is reinforced by Article 21A which mandates education for children. Employment of children below 14 years in any commercial establishment is illegal."
    },
    "can i start my own religion?": {
        "verdict": "YES",
        "articles": [{
            "article_no": "25; Freedom of Religion; All persons are equally entitled to freedom of conscience and the right to freely profess, practice and propagate religion",
            "title": "Freedom of Religion",
            "description": "All persons are equally entitled to freedom of conscience and the right to freely profess, practice and propagate religion"
        }],
        "reasoning": "Under Article 25 of the Constitution, every person has the freedom to profess, practice, and propagate their religion. This includes the right to establish new religious denominations, subject to public order, morality, and health."
    },
    "is smoking in public legal?": {
        "verdict": "NO",
        "articles": [{
            "article_no": "21; Right to Life and Personal Liberty; Protection of life and personal liberty includes right to clean environment",
            "title": "Right to Life",
            "description": "Protection of life and personal liberty includes right to clean environment"
        }],
        "reasoning": "Smoking in public places is prohibited under the Cigarettes and Other Tobacco Products Act (COTPA), 2003, which draws from Article 21's right to clean environment. This ban aims to protect public health and prevent passive smoking."
    }
}

def normalize_query(query):
    """Normalize query by removing extra spaces, punctuation, and converting to lowercase"""
    query = re.sub(r'[^\w\s]', '', query.lower())
    query = ' '.join(query.split())
    return query

def find_matching_demo_response(query):
    """Find matching demo response using more flexible matching"""
    normalized_query = normalize_query(query)
    
    if normalized_query in DEMO_RESPONSES:
        return DEMO_RESPONSES[normalized_query]
    
    key_phrases = {
        "marry a tree": "is it legal to marry a tree?",
        "marry tree": "is it legal to marry a tree?",
        "adopt 15": "can i adopt more than 15 children?",
        "adopt fifteen": "can i adopt more than 15 children?",
        "protest": "can i protest against the government?",
        "discriminate religion": "is it legal to discriminate based on religion?",
        "friend sue": "Can my friend sue me if I make fun of him for religion",
        "take property": "can the government take my property?",
        "child labor": "is child labor legal?",
        "child labour": "is child labor legal?",
        "start religion": "can i start my own religion?",
        "smoking public": "is smoking in public legal?",
        "smoke in public": "is smoking in public legal?"
    }
    
    for phrase, original_query in key_phrases.items():
        if phrase in normalized_query:
            return DEMO_RESPONSES[original_query]
    
    return None

def find_relevant_articles(query, threshold=SIMILARITY_THRESHOLD, top_k=3):
    """Find constitutional articles relevant to the query using cosine similarity."""
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
    """Generate a legal analysis summary based on the relevant constitutional articles."""
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
    """Determine a verdict (YES/NO/MAYBE) based on the constitutional articles."""
    if not articles:
        return "MAYBE"
    
    for article in articles:
        text = article.get('text', '').lower()
        if re.search(r'except\s+for\s+medicinal\s+purposes', text):
            return "YES"
    
    prohibited_terms = [r'\bprohibit\b', r'\billegal\b', r'\bforbid\b', r'\bban\b']
    for article in articles:
        text = article.get('text', '').lower()
        if any(re.search(term, text) for term in prohibited_terms):
            return "NO"
    
    permitted_terms = [r'\bright\b', r'\bpermit\b', r'\ballow\b', r'\blegal\b']
    for article in articles:
        text = article.get('text', '').lower()
        if any(re.search(term, text) for term in permitted_terms):
            return "YES"
    
    return "MAYBE"

def analyze_query_with_fallback(query):
    """Use fallback model for general legal reasoning."""
    prompt = (
        "You are a legal expert. Analyze the following legal query. "
        "Determine its legality and provide a verdict of YES, NO, or MAYBE. "
        "If applicable, cite any constitutional or statutory basis, otherwise state 'None'. "
        "Provide detailed judicial reasoning. "
        "Return ONLY a valid JSON object with exactly three keys: 'verdict', 'constitutional_basis', and 'judicial_reasoning'.\n\n"
        f"Query: {query}\n"
    )
    
    result = fallback_generator(prompt, max_length=512, do_sample=True, temperature=0.6)
    generated_text = result[0]['generated_text']
    
    try:
        json_match = re.search(r'(\{.*\})', generated_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
    except:
        pass
    
    return {
        "verdict": "MAYBE",
        "constitutional_basis": "None",
        "judicial_reasoning": "Likely no specific data related to the query in the constitution."
    }

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
        
        demo_response = find_matching_demo_response(situation)
        if demo_response:
            return jsonify(demo_response)
        
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

if __name__ == '__main__':
    app.run(debug=True)