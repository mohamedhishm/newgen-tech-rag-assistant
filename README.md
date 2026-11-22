# NewGen Tech – Company Knowledge Assistant

A production-style Retrieval-Augmented Generation (RAG) web application that helps employees find reliable answers to questions about company policies, HR, IT support, products, and internal procedures.

The application retrieves relevant information from **25 company documents**, generates grounded answers using an LLM, and displays the source documents so users can verify the information.

> **Course:** Computers and Society

---

## 1. Project Overview

Large Language Models (LLMs) store information learned during training in their parameters. This is known as *parametric memory*.

However, this information can become outdated and does not include private company documents. As a result, an LLM may produce inaccurate or fabricated answers when asked about internal company information.

This project addresses that problem using **Retrieval-Augmented Generation (RAG)**.

Instead of relying only on the model's training data, the application retrieves relevant passages from a local company knowledge base and provides them as context to the LLM.

### Key Features

- **Document-based Question Answering:** Answers questions using company documents.
- **Semantic Search:** Retrieves relevant passages using vector embeddings.
- **Source Citations:** Displays the documents and relevant passages supporting each answer.
- **Hallucination Reduction:** Uses a relevance threshold and a strict system prompt to avoid answering when sufficient context is unavailable.
- **Persistent Knowledge Base:** Stores document embeddings locally using ChromaDB.
- **Document Re-indexing:** Allows the knowledge base to be rebuilt after documents are updated.
- **System Health Monitoring:** Displays service status, document count, indexed chunks, model, and API key configuration.

---

## 2. RAG Architecture

The application follows a Retrieval-Augmented Generation pipeline:

```text
        Company Documents
        (25 files)
              |
              v
      [1] Document Loading
          load_documents()
              |
              v
      [2] Text Chunking
          RecursiveCharacterTextSplitter
          Chunk Size: 900
          Overlap: 150
              |
              v
      [3] Embeddings
          sentence-transformers/
          all-MiniLM-L6-v2
              |
              v
      [4] Vector Database
          ChromaDB
          Persistent Local Storage
              |
              v
      [5] Retrieval
          Similarity Search
          Top-K + Relevance Threshold
              |
              v
      [6] Context Validation
          Is relevant context available?
              |
         +----+----+
         |         |
        No        Yes
         |         |
         v         v
    Return       Groq LLM
    fallback     openai/gpt-oss-120b
    response         |
                     v
               Generated Answer
                     |
                     v
              Source Citations
                     |
                     v
                 Web UI
```

### Hallucination Reduction

The system uses several safeguards:

1. A strict system prompt instructs the LLM to answer only using the retrieved context.
2. A relevance threshold filters out weakly related results.
3. If no relevant context is retrieved, the LLM is not called.
4. Retrieved sources are displayed alongside answers for verification.

These safeguards reduce hallucinations but cannot guarantee that every generated answer is error-free.

---

## 3. Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Backend API | FastAPI | Handles application requests |
| Data Validation | Pydantic | Validates API inputs and outputs |
| RAG Orchestration | LangChain | Document processing and text splitting |
| Embedding Model | all-MiniLM-L6-v2 | Converts text into vector embeddings |
| Vector Database | ChromaDB | Stores and retrieves document embeddings |
| LLM Provider | Groq | Generates context-grounded answers |
| LLM Model | openai/gpt-oss-120b | Answer generation |
| Frontend | HTML, CSS, JavaScript | User interface |
| Testing | Pytest | Backend and RAG pipeline testing |

---

## 4. Project Structure

```text
newgen-tech-rag-assistant/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── rag_pipeline.py
│   └── services.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── data/
│   └── Company knowledge base documents
│
├── tests/
│   └── test_backend.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

The `vector_store/` directory is generated locally when the documents are indexed. It is excluded from Git because it can be rebuilt from the source documents.

---

## 5. Installation and Setup

### Requirements

- Python 3.10–3.12
- Git
- A Groq API key

### Step 1: Clone the Repository

```bash
git clone https://github.com/mohamedhishm/newgen-tech-rag-assistant.git
cd newgen-tech-rag-assistant
```

### Step 2: Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Copy the example environment file:

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

**Linux / macOS:**

```bash
cp .env.example .env
```

Add your Groq API key to `.env`:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Keep your actual `.env` file private. Never commit API keys to GitHub.

---

## 6. Running the Application

Start the FastAPI server:

```bash
uvicorn backend.main:app --reload
```

Open the application:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

On the first startup, the application loads the company documents, splits them into chunks, generates embeddings, and stores them in the local ChromaDB vector database.

The embedding model is downloaded locally when needed.

After modifying or adding documents, use the **Re-index documents** button in the sidebar to rebuild the knowledge base.

---

## 7. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Returns service and knowledge base status |
| POST | `/api/query` | Accepts a question and returns an answer with sources |
| POST | `/api/ingest` | Rebuilds the vector index from company documents |

### Example Query Request

```json
{
  "question": "How do I request IT support?"
}
```

### Example Response Structure

```json
{
  "answer": "Answer generated from company records...",
  "sources": [
    {
      "source": "25_IT_Helpdesk_Troubleshooting_FAQ.txt",
      "section": "IT Support",
      "score": 0.82,
      "snippet": "Relevant retrieved document passage..."
    }
  ],
  "grounded": true
}
```

The response values above are illustrative examples.

---

## 8. Configuration

The application can be configured through environment variables:

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key |
| `GROQ_MODEL` | LLM model identifier |
| `EMBEDDING_MODEL` | Sentence Transformers embedding model |
| `DATA_DIR` | Company documents directory |
| `VECTOR_STORE_DIR` | Local vector database directory |
| `CHUNK_SIZE` | Number of characters per text chunk |
| `CHUNK_OVERLAP` | Overlap between consecutive chunks |
| `TOP_K` | Maximum retrieved results |
| `MIN_RELEVANCE` | Minimum relevance threshold |

The actual default values are defined in `backend/config.py`.

---

## 9. Testing

Run the test suite using:

```bash
pytest -v
```

The tests cover the main backend and RAG functionality, including:

- Configuration handling.
- Document loading and chunking.
- Document ingestion.
- Retrieval ranking and relevance thresholds.
- Prompt construction.
- Handling questions without relevant context.
- API routes and request validation.

---

## 10. User Interface

The frontend is built using HTML, CSS, and vanilla JavaScript, without requiring a separate frontend build process.

The interface includes:

- A sidebar displaying system health and knowledge base statistics.
- Example questions for quick interaction.
- A chat interface for asking questions.
- Source details displayed with generated answers.
- A document re-indexing control.

### Color Palette

The interface uses a professional combination of:

- Beige: `#F3EBDD`
- Navy: `#192D48`
- Burgundy: `#79283D`
- Cream: `#FBF8F1`

---

## 11. Computers and Society Considerations

The project highlights several important considerations when deploying AI systems in workplace environments.

**Accuracy and Trust:** Employees may over-trust fluent AI-generated responses. Displaying source documents helps users verify information.

**Privacy:** Retrieved document passages are sent to the external Groq API for answer generation. Organizations should review their data-handling and privacy requirements before using confidential company information.

**Fairness:** Retrieval quality affects which company policies and procedures are presented to employees. Poor retrieval may lead to incomplete or misleading answers.

**Human Oversight:** Important HR, legal, or operational decisions should be verified against official company documents and responsible departments.

---

## 12. Future Improvements

Potential future enhancements include:

- Improved document retrieval and ranking.
- Hybrid search combining semantic and keyword retrieval.
- Conversation history and multi-turn question answering.
- More advanced evaluation of retrieval and answer quality.
- Authentication and role-based document access.
- Deployment to a production environment.

---

## License

This project was developed for educational purposes as part of the Computers and Society course.