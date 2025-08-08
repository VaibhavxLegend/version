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
  ```bash

- **Response:**

  ```json
  {
    "answers": [
      "The grace period is 30 days.",
      "The waiting period is 90 days."
    ]
  }
  ```bash

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

    ```web: python -m gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
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

## Cleaning Up & Customization

- All unused files, test scripts, and placeholder modules have been removed for a clean showcase.
- To add your own LLM or embedding service, extend `app/services/llm.py` and `app/services/embedding.py`.
- For advanced use (vector DB, auth, etc.), see commented stubs in `services/` and `security/`.

## License

MIT

---

**Showcase Ready:** This repo is now clean, production-ready, and easy to deploy or extend. Fork, star, and use as a template for your own document QA projects!
