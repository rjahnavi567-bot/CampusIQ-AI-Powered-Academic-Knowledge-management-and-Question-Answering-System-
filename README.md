# 🎓 CampusIQ:AI-Powered-Academic-Knowledge-management-and-Question-Answering-System

> An AI-powered Retrieval-Augmented Generation (RAG) platform that enables students and faculty to upload academic documents and receive accurate, context-aware answers grounded only in institutional learning resources.

---

## 📖 Project Overview

CampusIQ:AI-Powered-Academic-Knowledge-management-and-Question-Answering-System is a context-aware academic intelligence platform designed to improve the way students interact with educational resources. Unlike general-purpose AI assistants, this system answers questions **only from uploaded academic materials** such as textbooks, lecture notes, PowerPoint presentations, and documents.

The platform extracts text and images, generates semantic embeddings, stores them in a vector database, and retrieves the most relevant content before generating an AI response using Groq LLM.

---

## ✨ Key Features

- 📄 Upload PDF, DOCX, PPTX and TXT documents
- 🤖 AI-powered Question Answering using RAG
- 🔍 Hybrid Semantic Search with Cross-Encoder Re-ranking
- 🖼️ Automatic Image Extraction from textbooks
- 📝 OCR support for text-heavy images
- 📚 Subject-wise academic document organization
- 📊 Processing statistics and analytics dashboard
- 🕘 Question history with previous conversations
- 💾 PostgreSQL + ChromaDB storage architecture

---

## 🏗️ System Architecture

The platform follows a Retrieval-Augmented Generation pipeline.

<img src="Screenshots/End-to-End Architecture.png" alt="End-to-End Architecture" width="100%"/>

### Workflow

1. Upload academic documents
2. Extract text and images
3. Perform OCR when required
4. Generate semantic embeddings
5. Store vectors in ChromaDB
6. Retrieve relevant chunks
7. Re-rank using Cross Encoder
8. Generate grounded AI response

---

## 🛠️ Technology Stack

| Layer | Technology |
|--------|------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | FastAPI |
| Language | Python 3.11 |
| Database | PostgreSQL |
| Vector Database | ChromaDB |
| ORM | SQLAlchemy |
| AI Embeddings | BAAI BGE Small |
| Image Embeddings | CLIP ViT-B/32 |
| Caption Generation | Florence |
| OCR | Tesseract OCR |
| Image Processing | OpenCV, Pillow |
| LLM | Groq API |

---

## 📂 Project Structure

```text
AI-Academic-System/
│
├── backend/
│
├── frontend/
│
├── Screenshots/
|
|── testing/
|
|──.gitignore
|
|──LICENSE
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/AI-Academic-System.git
cd AI-Academic-System
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Environment

**Windows**

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a **.env** file inside the backend directory.

```env
DATABASE_URL=postgresql://username:password@localhost/academic_db

GROQ_API_KEY=your_groq_api_key

```

---

## ▶️ Running the Project

### Start Backend

```bash
cd backend
uvicorn main:app --reload
```

Open browser:

```
http://127.0.0.1:8000
```

---

# 📱 Application Screenshots

## 1. Dashboard

The dashboard provides an overview of uploaded documents, processing statistics, and quick navigation to every module.

<img src="Screenshots/Dashboard.png" alt="Dashboard" width="100%"/>

---

## 2. Upload Document

Users can upload academic documents, assign subjects, units, and rename files before processing.

<img src="Screenshots/PDF file successfully uploaded and saved with new title.png" alt="Upload Success" width="100%"/>

---

## 3. Uploaded Documents Page

Displays every uploaded document with subject information, upload status, and management actions.

<img src="Screenshots/Uploaded_documents_page.png" alt="Uploaded Documents" width="100%"/>

---

## 4. Documents Management

A complete table containing all uploaded academic resources.

<img src="Screenshots/Documents Page – A page with all uploaded files.png" alt="Documents Page" width="100%"/>

---

## 5. View Uploaded File

Users can open and read any uploaded academic document directly within the platform.

<img src="Screenshots/View Page result – A uploaded file opened after clicking view button.png" alt="View Document" width="100%"/>

---

## 6. AI Question Answering

Students ask questions in natural language, and the system retrieves the most relevant academic content before generating an answer.

<img src="Screenshots/Ask Page – Question & Answering Page.png" alt="Ask Page" width="100%"/>

---

## 7. Modern Ask Interface

The redesigned AI chat interface with semantic retrieval and grounded responses.

<img src="Screenshots/Ask_page.png" alt="Ask Interface" width="100%"/>

---

## 8. Question History

Stores previously asked questions and generated answers for future reference.

<img src="Screenshots/Question History Page – A Page containing all asked questions with answers.png" alt="Question History" width="100%"/>

---

## 9. Statistics Dashboard

Displays processing metrics including documents, chunks, embeddings, images, and execution statistics.

<img src="Screenshots/Statistics.png" alt="Statistics" width="100%"/>

---

## 10. Extracted Images

Visual content extracted automatically from uploaded academic textbooks.

<img src="Screenshots/Extracted images of uploaded file.png" alt="Extracted Images" width="100%"/>

---

## 11. Database Tables

### Documents Table

<img src="Screenshots/Documents Table Data.png" alt="Documents Table" width="100%"/>

### Document Images Table

<img src="Screenshots/document_images Table Data.png" alt="Document Images Table" width="100%"/>

---

# 📊 Performance Evaluation

## Average Processing Metrics

Average processing statistics generated for academic documents.

<img src="Screenshots/Average Processing Metrics per Document.png" alt="Average Processing Metrics" width="100%"/>

---

## Chunking Performance Analysis

Analysis of semantic chunk generation across uploaded resources.

<img src="Screenshots/Bar_Graph_of_Chunking Performance Analysis.png" alt="Chunking Analysis" width="100%"/>

---

## Document Upload Status

Distribution of successful and failed document uploads.

<img src="Screenshots/Pie_chart_Document Upload Status.png" alt="Upload Status" width="100%"/>

---

# 🗄️ Database Architecture

Logical design of PostgreSQL and ChromaDB integration.

<img src="Screenshots/Logical Database Design and Architecture.png" alt="Database Architecture" width="100%"/>

---

# 🔍 Retrieval Pipeline

The system combines multiple AI techniques for accurate retrieval.

| Stage | Description |
|--------|-------------|
| Text Extraction | PyMuPDF / DOCX / PPTX |
| OCR | Tesseract |
| Chunking | Semantic Paragraph Chunking |
| Embedding | BGE Small (384-dim) |
| Vector Search | ChromaDB |
| Re-ranking | Cross Encoder |
| Response | Groq LLM |

---

# 📈 Performance Highlights

| Metric | Value |
|---------|-------|
| Supported Formats | PDF, DOCX, PPTX, TXT |
| Vector Database | ChromaDB |
| Embedding Dimension | 384 |
| Image Embedding | 512 |
| OCR Engine | Tesseract |
| Backend Framework | FastAPI |
| Database | PostgreSQL |
| AI Response | Groq LLM |

---

# 🚀 Future Enhancements

- 🎥 Audio and Video lecture indexing
- 🌐 Multi-language academic support
- 📱 Mobile application
- 👨‍🏫 Faculty collaborative knowledge base
- ☁️ Cloud deployment with Docker
- 📖 Automatic citation generation

---

# 👩‍💻 Developer

**Reddy Jahnavi**

B.Tech Computer Science Engineering Student

CampusIQ:AI-Powered-Academic-Knowledge-management-and-Question-Answering-System —  A project for Quality Learning 

---

# 📄 License

This project is developed for educational and research purposes.

© 2026 Reddy Jahnavi. All Rights Reserved.
