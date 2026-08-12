from typing import Any
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def chunk_documents(documents: list[dict[str, Any]], words: int = 110) -> list[dict[str, Any]]:
    chunks = []
    for doc in documents:
        tokens = doc["text"].split()
        for start in range(0, len(tokens), words):
            body = " ".join(tokens[start:start + words])
            if body.strip():
                chunks.append({**doc, "chunk": body, "chunk_id": f"{doc['id']}-{start}"})
    return chunks

def retrieve(query: str, documents: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    chunks = chunk_documents(documents)
    if not chunks or not query.strip():
        return []
    corpus = [item["chunk"] for item in chunks]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(corpus + [query])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    results = []
    for index in scores.argsort()[::-1][:limit]:
        if scores[index] <= 0:
            continue
        item = dict(chunks[index])
        item["score"] = float(scores[index])
        results.append(item)
    return results

def relevant_sentence(text: str, query: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    terms = {term.lower() for term in re.findall(r"[a-zA-Z]{3,}", query)}
    ranked = sorted(sentences, key=lambda s: sum(term in s.lower() for term in terms), reverse=True)
    return (ranked[0] if ranked else text)[:360]
