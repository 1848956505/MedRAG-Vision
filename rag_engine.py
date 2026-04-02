import json
import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from config import Config
import jieba


class RAGEngine:
    def __init__(self):
        self.documents = []
        self.sources = []
        self.load_data()

        # 初始化稀疏检索 (BM25)
        tokenized_corpus = [list(jieba.cut(doc)) for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_corpus)

        # 初始化稠密检索 (FAISS + Embedding)
        self.embed_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        self.build_index()

    def load_data(self):
        try:
            with open(Config.KNOWLEDGE_DB_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.documents = [item['content'] for item in data]
                self.sources = [item['source'] for item in data]
        except Exception as e:
            print(f"知识库加载失败: {e}")
            self.documents = ["暂无数据"]
            self.sources = ["未知"]

    def build_index(self):
        if not self.documents: return
        embeddings = self.embed_model.encode(self.documents)
        self.index.add(np.array(embeddings).astype('float32'))

    def search(self, query, top_k=2):
        # 1. 稀疏检索 (BM25)
        tokenized_query = list(jieba.cut(query))
        bm25_scores = self.bm25.get_scores(tokenized_query)

        # 2. 稠密检索 (Vector)
        query_vec = self.embed_model.encode([query])
        D, I = self.index.search(np.array(query_vec).astype('float32'), top_k)

        # 3. 简单的结果合并 (这里简化了权重逻辑，优先取向量检索结果)
        results = []
        seen_docs = set()

        # 添加向量检索结果
        for idx in I[0]:
            if idx != -1 and idx < len(self.documents):
                doc = self.documents[idx]
                if doc not in seen_docs:
                    results.append({"content": doc, "source": self.sources[idx], "type": "vector"})
                    seen_docs.add(doc)

        # 添加 BM25 Top 1 补充
        top_bm25_idx = np.argmax(bm25_scores)
        doc = self.documents[top_bm25_idx]
        if doc not in seen_docs:
            results.append({"content": doc, "source": self.sources[top_bm25_idx], "type": "keyword"})

        return results[:top_k]


rag_engine = RAGEngine()