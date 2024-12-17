Here’s a well-structured `README.md` file for your FastAPI application:

```markdown
# FastAPI Semantic Search API

This FastAPI application provides endpoints for semantic search and managing text records in a vector database. The application supports searching for similar records, inserting new records, and deleting existing ones.

---

## Features
1. **Semantic Search**:
   - Perform semantic searches in a vector database.
   - Filter results by `class_type`.
   - Adjustable search parameters like `top_k` and `threshold`.

2. **Insert or Delete Records**:
   - Insert new text records into the database.
   - Delete existing records by `text_id`.

---

## Endpoints

### 1. `/semantic_search` (POST)
Perform a semantic search on the vector database.

#### Request Parameters:
- `search_text` *(str, required)*: The text to search for.
- `top_k` *(int, optional, default=100)*: The maximum number of similar records to retrieve. Must be between 1 and 10,000.
- `threshold` *(float, optional)*: The minimum similarity score (between 0.0 and 1.0).
- `class_type` *(str, required)*: The category of records to search in. Valid values: `All`, `class-a`, `class-b`.

#### Response:
Returns a list of similar records.

#### Error Handling:
- **400**: Invalid `top_k` or `threshold`.

---

### 2. `/inserting_or_deleting` (POST)
Insert or delete text records in the vector database.

#### Request Parameters:
- `text_id` *(int, required)*: The unique ID of the text record.
- `text` *(str, optional)*: The text content (required for insertion).
- `class_type` *(str, required)*: The category of the text. Valid values: `class-a`, `class-b`.
- `case` *(str, required)*: The operation to perform. Valid values: `insert`, `delete`.

#### Response:
- On success: A JSON object with the result of the operation.

#### Error Handling:
- **400**: Missing required parameters for insertion.

---

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- FastAPI and Uvicorn installed:
  ```bash
  pip install fastapi uvicorn
  ```

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the `utils.py` file is present in the project directory, with the following functions:
   - `search_vectorDB`: Handles semantic search logic.
   - `insert`: Adds a new record to the database.
   - `deleting`: Removes a record from the database.

### Run the Application
Start the FastAPI server:
```bash
uvicorn main:app --reload
```

Access the API documentation at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Project Structure
```
.
├── main.py              # FastAPI application
├── utils.py             # Utility functions (search_vectorDB, insert, deleting)
├── requirements.txt     # Dependencies
└── README.md            # Project documentation
```

---

## Example Usage

### Semantic Search
```bash
curl -X POST "http://127.0.0.1:8000/semantic_search" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "search_text=example query&top_k=50&class_type=class-a"
```

### Insert Record
```bash
curl -X POST "http://127.0.0.1:8000/inserting_or_deleting" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "text_id=123&text=example text&class_type=class-a&case=insert"
```

### Delete Record
```bash
curl -X POST "http://127.0.0.1:8000/inserting_or_deleting" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "text_id=123&class_type=class-a&case=delete"
```

---

## License
This project is licensed under the MIT License.

---

## Acknowledgments
Special thanks to all contributors and maintainers of FastAPI for providing a robust and modern framework for building APIs.
```

This `README.md` provides clear setup instructions, usage examples, and details about each endpoint. Let me know if you need further refinements!