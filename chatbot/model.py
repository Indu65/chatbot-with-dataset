# model.py
import os
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

class ChatbotModel:
    def __init__(self, data_path='data/dataset.txt', min_similarity=0.2, persist_path='data/model.joblib'):
        self.data_path = data_path
        self.min_similarity = min_similarity
        self.persist_path = persist_path
        self.vectorizer = None
        self.doc_vectors = None
        self.questions = []
        self.answers = []
        self._load_or_build()

    def _load_or_build(self):
        # Try loading cached model
        try:
            if os.path.exists(self.persist_path):
                saved = joblib.load(self.persist_path)
                self.vectorizer = saved['vectorizer']
                self.doc_vectors = saved['doc_vectors']
                self.questions = saved['questions']
                self.answers = saved['answers']
                print("✅ Loaded cached model from", self.persist_path)
                return
        except Exception as e:
            print("⚠️ Could not load cached model:", e)

        # Read dataset
        with open(self.data_path, 'r', encoding='utf-8') as f:
            text = f.read()

        qs, ans = self._parse_dataset(text)
        if not qs:
            raise ValueError("❌ No usable data parsed from dataset file. Check dataset formatting.")

        self.questions = qs
        self.answers = ans
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words='english', max_features=5000)
        self.doc_vectors = self.vectorizer.fit_transform(self.questions)

        # Save cache
        try:
            joblib.dump({
                'vectorizer': self.vectorizer,
                'doc_vectors': self.doc_vectors,
                'questions': self.questions,
                'answers': self.answers
            }, self.persist_path)
        except Exception as e:
            print("⚠️ Warning: could not save model cache:", e)

    def _parse_dataset(self, text):
        """
        Parse dataset into Q/A pairs.
        Supports:
        - Tab-separated (Question<TAB>Answer)
        - Space-based splitting (Q? A..., Q. A...)
        - Fallback: each line as both Q and A
        """
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        qs, ans = [], []
        for l in lines:
            if '\t' in l:  # case 1: tab
                q, a = l.split('\t', 1)
                qs.append(q.strip())
                ans.append(a.strip())
            elif "? " in l:  # case 2: question mark
                q, a = l.split("? ", 1)
                qs.append(q.strip() + "?")
                ans.append(a.strip())
            elif ". " in l:  # case 3: period
                q, a = l.split(". ", 1)
                qs.append(q.strip() + ".")
                ans.append(a.strip())
            else:  # fallback
                qs.append(l)
                ans.append(l)
        return qs, ans

    def get_response(self, user_text):
        if not user_text or not user_text.strip():
            return "Please type something."

        q_vec = self.vectorizer.transform([user_text])
        scores = cosine_similarity(q_vec, self.doc_vectors)[0]
        best_idx = int(np.argmax(scores))
        best_score = float(scores[best_idx])

        if best_score >= self.min_similarity:
            return self.answers[best_idx]
        else:
            return f"I'm not sure, but maybe this helps:\n\n{self.answers[best_idx]}"

if __name__ == '__main__':
    model = ChatbotModel(data_path='data/dataset.txt')
    while True:
        txt = input("You: ")
        print("Bot:", model.get_response(txt))
