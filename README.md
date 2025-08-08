# HackRX LLM Query System

A robust, production-ready FastAPI application for document-based question answering, designed for hackathons and real-world deployments. This project processes PDF documents, extracts text, and answers user questions using a custom LLM service, with a focus on reliability, speed, and minimal dependencies.

## Features

- **FastAPI** backend with CORS enabled for easy integration
- **Manual request validation** (no Pydantic required)
- **PDF text extraction** using PyPDF2
- **LLM service** for concise, single-line, plain-text answers
- **Threaded parallel question answering** for speed
- **Aggressive output sanitization** (no markdown, no newlines)
- **Production-ready deployment** (Gunicorn + UvicornWorker, Render/Cloud/Container)
- **Health check endpoint**

## Technologies Used

- Python 3.10+
- FastAPI
- Uvicorn
- Gunicorn
- PyPDF2
- Requests
- (Optional) Google Gemini API for LLM (or plug in your own)

## API Overview

### POST `/hackrx/run`

- **Headers:** `Authorization: Bearer <HACKATHON_TOKEN>`
- **Body:**

  ```json
  {
    "documents": "<PDF_URL>",
    "questions": ["What is the grace period?", "What is the waiting period?"]
  }
  ```

- **Response:**

  ```json
  {
    "answers": [
      "The grace period is 30 days.",
      "The waiting period is 90 days."
    ]
  }
  ```

### GET `/health`

- Returns service health status.

## Pipeline & Deployment

- **Local:**

  ```bash
  pip install -r requirements.txt
  uvicorn app.main:app --host 0.0.0.0 --port 8000
  ```

- **Production:**

  - Uses `Procfile` for Render/Heroku/Cloud Run:

    ```bash
    python -m gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
    ```

  - Dockerfile provided for containerized deployment.

## Environment Variables

- `HACKATHON_TOKEN` (required): Bearer token for API access
- `GEMINI_API_KEY` (optional): API key for Gemini LLM (if used)

## Project Structure

```csharp
app/
  main.py                # FastAPI app entrypoint
  api/endpoints_no_pydantic.py  # Main API endpoints (no Pydantic)
  models/manual_schemas.py      # Manual request/response validation
  services/llm.py        # LLM service (single-line answers)
  services/pdf_processing.py    # PDF text extraction
  ...
requirements.txt         # Python dependencies
Procfile                 # Production process definition
Dockerfile               # Container build
README.md                # Project documentation
```

## How It Works

1. User submits a PDF URL and questions to `/hackrx/run` with the correct token.
2. The server downloads and extracts text from the PDF.
3. Each question is answered in parallel using the LLM service, with strict output sanitization.
4. Answers are returned as a JSON array.

## Customization

- To add your own LLM or embedding service, extend `app/services/llm.py` and `app/services/embedding.py`.
- For advanced use (vector DB, auth, etc.), see commented stubs in `services/` and `security/`.

## Future Scope

- **Enhanced LLM Integration:** Support for multiple LLM providers with dynamic selection based on user preferences or performance metrics.
- **Vector Database Integration:** Add support for vector databases like Pinecone or Weaviate for advanced document search and retrieval.
- **Authentication Enhancements:** Implement OAuth2 or JWT-based authentication for improved security.
- **Real-Time Collaboration:** Enable multiple users to interact with the system simultaneously with session management.
- **Multi-Language Support:** Extend the system to support document processing and question answering in multiple languages.
- **Improved PDF Parsing:** Incorporate advanced PDF parsing libraries for better handling of complex document layouts.
- **UI/UX Development:** Build a user-friendly web interface for easier interaction with the system.
- **Cloud-Native Features:** Add support for serverless deployments and auto-scaling on platforms like Azure Functions or AWS Lambda.
- **Analytics Dashboard:** Provide insights into system usage, performance, and user behavior through an integrated dashboard.
- **Offline Mode:** Enable offline processing of documents and questions for environments with limited internet connectivity.