# 🤖 PDF AI Assistant

An AI-powered PDF Document Assistant that allows users to ask questions from a PDF and get intelligent answers using **RAG (Retrieval Augmented Generation)**.

## 🚀 Features

- 📄 Chat with PDF documents
- 💬 Ask questions and get AI answers
- 🔍 Semantic search using embeddings
- 🧠 Context-based answers to reduce hallucination
- ⚡ Powered by Google Gemini AI
- 🌐 Web interface using Flask

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### AI / ML
- LangChain
- Google Gemini API
- HuggingFace Embeddings
- ChromaDB

## ⚙️ How It Works

1. PDF document is loaded
2. Text is split into smaller chunks
3. Text chunks are converted into embeddings
4. Embeddings are stored in Chroma Vector Database
5. User questions are matched with relevant content
6. Gemini AI generates the final response

## 📂 Project Structure
