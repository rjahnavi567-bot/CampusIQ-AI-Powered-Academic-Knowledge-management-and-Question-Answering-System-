## 🚧 Development Status

**Project Status:** Active Development

AI-Academic-System is currently under active development. Core functionalities such as document ingestion, OCR processing, text extraction, chunking, embedding generation, vector storage, and semantic retrieval are being implemented and tested.

### Current Progress

✅ Project architecture finalized

✅ FastAPI backend setup

✅ Document processing pipeline implementation

✅ OCR integration using Tesseract

✅ Embedding generation pipeline

✅ Vector database integration (FAISS)

✅ Initial RAG workflow design

✅ Duplicate document detection module

✅ Advanced semantic search optimization

✅ LLM integration and response generation

🔄 Frontend development

⏳ User authentication and authorization

⏳ Knowledge graph generation

⏳ Multi-user support

### Note

This repository is currently a work in progress. Features, APIs, folder structures, and implementation details may change as development continues. Contributions, suggestions, and feedback are welcome.

# CampusIQ – AI-Powered Academic Knowledge management and Question Answering System 

An AI-powered Academic Knowledge Management and Question Answering System designed to help students, researchers, and faculty interact with academic documents using Natural Language Processing (NLP), Retrieval-Augmented Generation (RAG), Semantic Search, and Large Language Models (LLMs).

---

## Overview

CampusIQ – AI-Powered Academic Knowledge management and Question Answering System  enables users to upload academic resources such as:

* PDF files
* PowerPoint presentations (PPT/PPTX)
* Word documents (DOC/DOCX)
* Scanned documents
* Images containing text

The system automatically extracts content, performs OCR when required, generates embeddings, stores them in a vector database, and allows users to ask natural language questions over their academic content.

The platform is designed to serve as an intelligent academic assistant capable of document search, concept discovery, and contextual question answering.

---

# Key Objectives

* Centralized academic knowledge repository
* Semantic search across academic resources
* AI-powered question answering
* Duplicate document detection
* OCR support for scanned documents
* Multi-format document ingestion
* Retrieval-Augmented Generation (RAG)
* Scalable architecture for future enhancements

---

# System Architecture

## High-Level Architecture

```
                +------------------+
                |      User        |
                +---------+--------+
                          |
                          v
                +------------------+
                | Frontend UI      |
                +---------+--------+
                          |
                          v
                +------------------+
                | FastAPI Backend  |
                +---------+--------+
                          |
        ----------------------------------
        |                |               |
        v                v               v

+---------------+ +--------------+ +-------------+
| File Upload   | | Query Engine | | Admin APIs  |
+-------+-------+ +------+-------+ +-------------+
        |                |
        v                v

+------------------------------------------+
| Document Processing Pipeline             |
+------------------------------------------+
        |
        v

+------------------+
| Text Extraction  |
+------------------+
        |
        +---------------------+
        |                     |
        v                     v

+---------------+   +-------------------+
| Native Text   |   | OCR Processing    |
| Extraction    |   | (Tesseract OCR)   |
+---------------+   +-------------------+

        |
        v

+-------------------+
| Text Cleaning     |
+-------------------+

        |
        v

+-------------------+
| Chunking Engine   |
+-------------------+

        |
        v

+-------------------+
| Embedding Model   |
+-------------------+

        |
        v

+-------------------+
| Vector Database   |
+-------------------+

        |
        v

+-------------------+
| Semantic Search   |
+-------------------+

        |
        v

+-------------------+
| LLM Response      |
+-------------------+
```

---

# Document Processing Flow

1. User uploads document.
2. System detects document type.
3. Extract text from document.
4. If scanned/image-based:

   * Convert pages to images.
   * Run OCR.
5. Clean extracted text.
6. Generate chunks.
7. Create embeddings.
8. Store embeddings in vector database.
9. Store metadata.
10. Document becomes searchable.

---

# Query Processing Flow

1. User asks question.
2. Query embedding generated.
3. Vector search performed.
4. Relevant chunks retrieved.
5. Context assembled.
6. LLM generates answer.
7. Sources returned with response.

---

# Current Features

## Document Management

* PDF Upload
* DOCX Upload
* PPT/PPTX Upload
* Image Upload
* Metadata Storage

## Text Extraction

* PDF text extraction
* DOCX extraction
* PPT extraction
* OCR for scanned PDFs
* OCR for images

## OCR Support

* Tesseract OCR Integration
* Image preprocessing
* Scanned document handling

## Text Processing

* Cleaning and normalization
* Chunk generation
* Metadata tagging

## Embeddings

* Sentence Transformer embeddings
* Batch embedding generation
* Vector indexing

## Semantic Search

* Similarity search
* Context retrieval
* Academic content discovery

## AI Question Answering

* Retrieval-Augmented Generation (RAG)
* Context-aware responses
* Source-backed answers

## Backend

* FastAPI APIs
* REST endpoints
* Modular architecture

---

# Planned Features

## Duplicate Detection

* Exact duplicate detection
* Near-duplicate detection
* Semantic duplicate detection

## Advanced Search

* Hybrid Search
* Keyword + Semantic Search
* Metadata Filtering

## User Features

* Authentication
* Role-based Access Control
* User-specific document collections

## Academic Enhancements

* Citation extraction
* Reference linking
* Topic clustering
* Knowledge graph generation

## AI Enhancements

* Local LLM support
* Multi-LLM support
* Conversation memory
* Academic summarization

---

# Technology Stack

## Backend

* Python 3.11
* FastAPI
* Uvicorn

## AI / NLP

* Sentence Transformers
* Transformers
* LangChain (Optional)
* Gemini API (Optional)
* OpenAI API (Optional)

## OCR

* Tesseract OCR
* OpenCV
* Pillow

## Document Processing

* PyMuPDF
* python-docx
* python-pptx

## Vector Database

* FAISS

## Data Handling

* NumPy
* Pandas

---

# Project Structure

```
AI-Academic-System/

├── backend/
│   ├── api/
│   ├── services/
│   ├── ingestion/
│   ├── embeddings/
│   ├── vector_store/
│   ├── rag/
│   ├── ocr/
│   ├── duplicate_detection/
│   └── main.py
│
├── frontend/
│
├── uploads/
│
├── vector_db/
│
├── models/
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

# Setup Instructions

## Prerequisites

Install:

* Python 3.11
* Git
* Tesseract OCR

---

## Clone Repository

```bash
git clone https://github.com/<your-username>/AI-Academic-System.git

cd AI-Academic-System
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Tesseract OCR

### Windows

Download and install:

https://github.com/UB-Mannheim/tesseract/wiki

Verify:

```bash
tesseract --version
```

---

## Run Backend

```bash
uvicorn main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

# Future Roadmap

Phase 1

* Document ingestion
* OCR
* Embeddings
* Vector storage

Phase 2

* Semantic search
* RAG pipeline
* AI-powered Q&A

Phase 3

* Duplicate detection
* Hybrid search
* Metadata filtering

Phase 4

* Authentication
* Multi-user support
* Knowledge graphs

Phase 5

* Academic copilot
* Personalized learning assistant
* Research recommendation engine

---

# Contributors

AI-Academic-System is being developed as an academic AI platform focused on intelligent document understanding, semantic retrieval, and educational assistance.

---

# License

MIT License
