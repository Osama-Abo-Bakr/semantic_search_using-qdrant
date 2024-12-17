# Import Library
from fastapi import FastAPI, Form, HTTPException
from utils import search_vectorDB, insert, deleting



# Initialize FastAPI
app = FastAPI(debug=True)

@app.post('/semantic_search')
async def search(search_text: str=Form(...), top_k: int=Form(100), 
                          threshold: float=Form(None), class_type: str=Form(..., description='class_type', enum=['All', 'class-a', 'class-b'])):

    ## Validation for top_k, and threshold
    if top_k <= 0 or not isinstance(top_k, int) or top_k > 10000 or top_k is None:
        raise HTTPException(status_code=400, detail="Bad Request: 'top_k' must be a positive integer and less than 10000.")
    
    elif threshold is not None and (threshold <= 0.0 or not isinstance(threshold, float) or threshold > 1.0):
        raise HTTPException(status_code=400, 
                            detail="Bad Request: 'threshold' must be a positive float greater than 0.0 and less than 1.0")

    else:
        ## Get Similar Records --> Call the (search_vectDB) from utils.py
        similar_records = search_vectorDB(query_text=search_text, top_k=top_k,
                                        threshold=threshold, class_type=class_type)

        return similar_records
    
    
    
    
@app.post('/inserting_or_deleting')
async def insert_delete(text_id: int=Form(...),
                        text: str=Form(None),
                        class_type: str=Form(..., description='class_type', enum=['class-a', 'class-b']),
                        case: str=Form(..., description='case', enum=['insert', 'delete'])):
    
    if case == 'insert' and (not text or not class_type):
        raise HTTPException(status_code=400, detail="Bad Request: 'text' and 'class_type' are required for insertion.")
    
    
    if case == 'insert':
        result = insert(text_id=text_id, text=text, class_type=class_type)

    elif case == 'delete':
        result = deleting(text_id=text_id)
        
    return {'result': result}