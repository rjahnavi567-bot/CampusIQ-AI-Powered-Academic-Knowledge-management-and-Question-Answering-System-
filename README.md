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

# 📸 Application Screenshots
1. Dashboard

The central homepage of the AI Academic System showing quick navigation, document statistics, and an overview of the platform's modules.

Screenshot: Dashboard.png

2. Document Upload

Demonstrates the successful upload and renaming of an academic PDF before it is processed by the system.

Screenshot: PDF file successfully uploaded and saved with new title.png

3. Uploaded Documents

Displays all uploaded academic resources along with subject information, upload status, and document management options.

Screenshot: Uploaded_documents_page.png

4. Documents Management Page

A complete table view of every uploaded document, including metadata and available actions such as view and delete.

Screenshot: Documents Page – A page with all uploaded files.png

5. Document Viewer

Shows the built-in viewer used to open and read uploaded academic documents directly within the application.

Screenshot: View Page result – A uploaded file opened after clicking view button.png

6. AI Question Answering

Illustrates how users ask academic questions and receive answers generated from the retrieved course materials.

Screenshot: Ask Page – Question & Answering Page.png

7. Modern Ask Interface

The redesigned conversational interface providing semantic retrieval and context-aware AI responses.

Screenshot: Ask_page.png

8. Question History

Stores previously asked questions and their generated answers, allowing users to revisit earlier conversations.

Screenshot: Question History Page – A Page containing all asked questions with answers.png

9. Statistics Dashboard

Presents processing metrics including documents, chunks, embeddings, extracted images, and overall system analytics.

Screenshot: Statistics.png

10. Extracted Images

Shows the images automatically extracted from uploaded textbooks and lecture materials during document processing.

Screenshot: Extracted images of uploaded file.png

# 📊 Performance & Architecture Figures
End-to-End Architecture

Illustrates the complete Retrieval-Augmented Generation (RAG) workflow from document upload to AI response generation.

Figure: End-to-End Architecture.png

Logical Database Architecture

Represents the relationship between PostgreSQL, ChromaDB, documents, chunks, and image storage.

Figure: Logical Database Design and Architecture.png

Average Processing Metrics

Visualizes the average number of pages, chunks, embeddings, and extracted images processed per academic document.

Figure: Average Processing Metrics per Document.png

Chunking Performance Analysis

Bar graph comparing semantic chunk generation and processing performance across documents.

Figure: Bar_Graph_of_Chunking Performance Analysis.png

Document Upload Status

Pie chart showing the distribution of successful and failed document upload attempts.

Figure: Pie_chart_Document Upload Status.png

# Database Tables

Documents Table: Stores uploaded document metadata.

Document Images Table: Stores extracted images, captions, and classification details.

Figures: Documents Table Data.png, document_images Table Data.png

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
