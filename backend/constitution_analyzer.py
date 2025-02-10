import torch
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import pandas as pd
from cachetools import TTLCache
from typing import List, Dict, Tuple
from models import Article, Response

class ConstitutionAnalyzer:
    def __init__(self):
        self.cache = TTLCache(maxsize=1000, ttl=3600)
        self.constitution_df = pd.read_csv('data/constitution_of_india.csv')
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        self._initialize_models()
        self._compute_article_embeddings()

    def _initialize_models(self):
        print("Loading AI models...")
        self.zero_shot_classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=0 if torch.cuda.is_available() else -1
        )
        self.legal_analyzer = pipeline(
            "text-classification",
            model="nlpaueb/legal-bert-base-uncased",
            device=0 if torch.cuda.is_available() else -1
        )
        self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.similarity_model.to(self.device)

    def _compute_article_embeddings(self):
        print("Computing constitutional embeddings...")
        self.article_embeddings = self.similarity_model.encode(
            self.constitution_df['content'].tolist(),
            convert_to_tensor=True,
            show_progress_bar=True
        )
        self.article_embeddings = self.article_embeddings.to(self.device)

    def analyze_situation(self, situation: str) -> Response:
        cache_key = situation.lower().strip()
        if cache_key in self.cache:
            return self.cache[cache_key]

        relevant_articles = self._find_relevant_articles(situation)
        verdict, confidence, reasoning = self._batch_analyze_legality(situation, relevant_articles)
        loopholes = self._generate_loopholes(situation, relevant_articles)

        response = Response(
            verdict=verdict,
            articles=relevant_articles,
            reasoning=reasoning,
            loopholes=loopholes,
            confidence=confidence
        )

        self.cache[cache_key] = response
        return response

    def _find_relevant_articles(self, situation: str) -> List[Article]:
        situation_embedding = self.similarity_model.encode(
            situation, 
            convert_to_tensor=True
        ).to(self.device)

        similarities = torch.cosine_similarity(
            situation_embedding.unsqueeze(0),
            self.article_embeddings
        )

        top_indices = torch.argsort(similarities, descending=True)[:3]
        relevant_articles = []
        for idx in top_indices:
            row = self.constitution_df.iloc[idx]
            article = Article(
                article_number=row['article_number'],
                title=row['title'],
                content=row['content'],
                similarity_score=similarities[idx].item()
            )
            relevant_articles.append(article)

        return relevant_articles

    def _batch_analyze_legality(
        self, 
        situation: str, 
        articles: List[Article]
    ) -> Tuple[str, float, str]:
        if not articles:
            return "MAYBE", 0.5, "No directly relevant constitutional provisions found."

        legal_future = torch.jit.fork(lambda: self.legal_analyzer(
            situation,
            truncation=True,
            max_length=512
        ))

        zero_shot_future = torch.jit.fork(lambda: self.zero_shot_classifier(
            situation,
            candidate_labels=["constitutional", "unconstitutional", "legally ambiguous"],
            hypothesis_template="This situation is {}."
        ))

        legal_analysis = torch.jit.wait(legal_future)
        zero_shot_result = torch.jit.wait(zero_shot_future)

        scores = dict(zip(zero_shot_result['labels'], zero_shot_result['scores']))
        max_confidence = max(zero_shot_result['scores'])

        if scores['constitutional'] > 0.6:
            verdict = "YES"
            reasoning = (
                f"Analysis suggests this is constitutionally protected. "
                f"Key article: {articles[0].article_number}"
            )
        elif scores['unconstitutional'] > 0.6:
            verdict = "NO"
            reasoning = (
                f"This appears to conflict with constitutional provisions. "
                f"See {articles[0].article_number} for details."
            )
        else:
            verdict = "MAYBE"
            reasoning = (
                "This falls into a constitutional grey area. "
                "Multiple interpretations possible based on context."
            )

        return verdict, max_confidence, reasoning

    def _generate_loopholes(self, situation: str, articles: List[Article]) -> List[str]:
        if not articles:
            return ["No clear loopholes found"]

        loophole_hypotheses = [
            "This could be protected as a fundamental right",
            "This might qualify as an exception under",
            "This could be interpreted as exercise of constitutional rights",
            "This might fall under reasonable restrictions",
            "This could be viewed as a matter of public interest"
        ]

        result = self.zero_shot_classifier(
            situation,
            candidate_labels=loophole_hypotheses,
            multi_label=True
        )

        loopholes = []
        for label, score in zip(result['labels'], result['scores']):
            if score > 0.3:
                article = articles[0].article_number
                loophole = f"{label} under {article}"
                loopholes.append(loophole)

        return loopholes if loopholes else ["No obvious loopholes found"]

    def batch_analyze_situations(self, situations: List[str]) -> List[Response]:
        responses = []
        batch_size = 4

        for i in range(0, len(situations), batch_size):
            batch = situations[i:i + batch_size]
            batch_responses = []

            for situation in batch:
                response = self.analyze_situation(situation)
                batch_responses.append(response)

            responses.extend(batch_responses)

        return responses