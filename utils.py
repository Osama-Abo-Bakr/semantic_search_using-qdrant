## Import Libraries
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from fastapi import HTTPException
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, PointIdsList, Filter, FieldCondition, MatchValue

## Load dotenv file
_ = load_dotenv(override=True)
qdrant_key = os.getenv('QDRANT_API_KEY')
qdrant_url = os.getenv('QDRANT_URL')
collec_name = 'course'

## Connect to Qdrant Client
client = QdrantClient(url=qdrant_url, api_key=qdrant_key, timeout=80) ## Increase TimeOut if the retrieving is too much

## Load the Model
model_hugging = SentenceTransformer(model_name_or_path='all-MiniLM-L6-v2', device='cpu')


def search_vectorDB(query_text: str, top_k: int=5, threshold: float=0.25, class_type: str=None):
    try:
        embedding_query = model_hugging.encode(query_text).tolist()
        if class_type in ['class-a', 'class-b']: 
            results = client.search(collection_name=collec_name, query_vector=embedding_query,
                        limit=top_k, score_threshold=threshold,
                        query_filter=Filter(must=[FieldCondition(key='class', match=MatchValue(value=class_type))]))
            
        else:
            results = client.search(collection_name=collec_name, query_vector=embedding_query,
                        limit=top_k, score_threshold=threshold)
            
        results = [{'id': int(point.id), 'score': float(point.score), 'class': point.payload['class']} for point in results]
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    

def insert(text_id: int, text: str, class_type: str):
    try:
        embedding_text = model_hugging.encode(text).tolist()
        
        _ = client.upsert(collection_name=collec_name, wait=True,
                    points=[PointStruct(id=text_id, vector=embedding_text, 
                                        payload={'class': class_type})])
        
        return f"Count After Upsert: {client.get_collection(collection_name=collec_name).points_count}"
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
def deleting(text_id: int):
    try:
        _ = client.delete(collection_name=collec_name,
                          points_selector=PointIdsList(points=[text_id]))
        
        return f"Count After Deletion: {client.get_collection(collection_name=collec_name).points_count}"
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))