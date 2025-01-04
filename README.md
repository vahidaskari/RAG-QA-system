
# RAG-based QA System

## Description

The RAG-based QA System is a question-answering application that leverages Retrieval-Augmented Generation (RAG) to provide accurate and contextually relevant answers. It combines the power of retrieval-based models and generative models to enhance the quality of responses. The system supports file uploads, asking question, and logs management to deliver a seamless user experience.

## Installation

### Prerequisites

- Python 3.8 or higher
- Docker (optional, for containerized deployment)
- MongoDB

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/vahidaskari/RAG-QA-system
    ```
2. Navigate to the project directory:
    ```bash
    cd RAG-QA-system
    ```
3. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Install the required dependencies:
    ```bash
    pip install -r requirements.lock
    ```

## Configuration

Before running the application, copy the `.env.sample` file to `.env` and update the environment variables based on your setup:
```bash
cp .env.sample .env
```

## Usage

To start the QA system, use the following command:
```bash
fastapi run
```

## Docker Deployment

Build and run the application using Docker:
```bash
docker build -t rag_app .
docker run --rm --name rag-app -p 127.0.0.1:8000:8000 --network host --env-file ./.env -v ./../data:/app/data rag_app
```
## Docker compose Deployment (Recommended)
1. change the MONGODB_CONNECTION_STRING value to "mongodb://mongodb:27017/" in `.env` file\
2. run:
```bash
docker compose up
```

## API Routes

### 1. **Upload File**

Upload one or more files for processing. Files are saved, and text is extracted to create a document stored in ChromaDB.

- **Endpoint**: `POST /file`
- **Description**: Uploads multiple files and returns a unique `document_id` to reference the stored documents.
- **Request**:
  - Form-data: `documents` (list of files)
- **Response**:
  - `{"document_id": "<unique_document_id>"}`
- **Example**:
  ```bash
  curl -X POST "http://127.0.0.1:8000/file" -F "documents=@example.pdf"
  ```

---

### 2. **Chat**

Send a query and receive a response based on the provided document context.

- **Endpoint**: `POST /chat`
- **Description**: Retrieves context from the document and generates a response using an LLM.
- **Request Body**:
  ```json
  {
    "query": "What is the content of the uploaded file?",
    "document_id": "<unique_document_id>"
  }
  ```
- **Response**:
  ```json
  {
    "response": "<generated_response>"
  }
  ```
- **Example**:
  ```bash
  curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d '{"query":"What is in the file?","document_id":"12345"}'
  ```

---

### 3. **Logs**

Retrieve logs or records of interactions with the system.

- **Endpoint**: `POST /logs`
- **Description**: Fetches logs for a specific document or all logs if no `document_id` is provided (to get all logs, send an empty JSON as body). here, "document_id" refers to mongodb document id (_id) .
- **Request Body**:
  ```json
  {
    "document_id": "<optional_document_id>"
  }

  ```
- **Response**:
  - Single log: `{ ...log_data... }`
  - Multiple logs: `[ ...list_of_log_data... ]`
- **Example**:
  ```bash
  curl -X POST "http://127.0.0.1:8000/logs" -H "Content-Type: application/json" -d '{"document_id":"12345"}'
  ```
