# 🎓 TutorAI

> **An AI-powered study assistant that lets you chat with your PDFs and enrich responses with real-time web search.**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-Deployed-red?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/LangChain-RAG-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Groq-Llama--3.3--70B-orange?style=for-the-badge" />
</p>

---

## 📖 Overview

TutorAI is a Retrieval-Augmented Generation (RAG) application that enables users to upload PDFs, build a semantic knowledge base, and interact with their documents through natural conversation.

It also supports **optional web search**, allowing answers to be enhanced with recent information while always prioritizing the user's uploaded notes.

---

## ✨ Features

- 📄 Upload multiple PDF documents
- 💬 Chat naturally with your notes
- 🌐 Optional web search using Tavily
- 🧠 RAG-powered semantic retrieval
- 📚 ChromaDB vector database
- 🔍 FAISS similarity search
- 📝 Conversation memory for follow-up questions
- 🤖 Powered by Groq's Llama 3.3 70B
- 🎨 Modern Streamlit interface

---

## 🏗️ Architecture

```
                  ┌──────────────┐
                  │ Upload PDFs  │
                  └──────┬───────┘
                         │
                  PDF Processing
                         │
                Text Chunking
                         │
                 HuggingFace Embeddings
                         │
                    ChromaDB
                         │
                  Similarity Search
                         │
         Optional Tavily Web Search
                         │
                 Context Retrieval
                         │
             Groq Llama 3.3 70B
                         │
                  Final Response
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Frontend | Streamlit |
| LLM | Groq (Llama 3.3 70B) |
| Framework | LangChain |
| Embeddings | HuggingFace (`all-MiniLM-L6-v2`) |
| Vector Store | ChromaDB |
| Retrieval | FAISS |
| Web Search | Tavily API |
| PDF Loader | PyPDF |
| Language | Python |

---

## 📂 Project Structure

```text
TutorAI/
│
├── Data/                 # Uploaded PDFs
├── db/                   # Vector Database
├── app.py                # Streamlit UI
├── sample.py             # RAG Pipeline
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/snehit20/TutorAI.git
cd TutorAI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory.

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

If deploying on **Streamlit Community Cloud**, add these variables under **App Settings → Secrets**.

---

## ▶️ Run the application

```bash
streamlit run app.py
```

---

## 📸 Demo

### Live Demo

🔗 **https://YOUR-STREAMLIT-LINK.streamlit.app**

*(Replace this with your deployed URL.)*

---

## 💡 How It Works

1. Upload one or more PDFs.
2. (Optional) Enter a topic for web search.
3. Build the knowledge base.
4. Ask questions naturally.
5. TutorAI retrieves relevant information from your PDFs (and optionally the web) to generate accurate responses.

---

## 🔮 Future Improvements

- 📑 DOCX & PPT support
- 🖼️ Image understanding
- 📖 Source citations
- 💾 Persistent conversations
- 👤 User authentication
- 📤 Chat export
- 🌍 Multi-language support

---

## 🤝 Contributing

Contributions, ideas, and feature requests are always welcome.

If you'd like to improve TutorAI, feel free to fork the repository and submit a pull request.

---

## 👨‍💻 Author

**Snehit Singh**

- GitHub: https://github.com/snehit20
- LinkedIn: *(Add your LinkedIn profile)*

---

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star**.

It helps others discover the project and motivates future development.

---

<p align="center">
Made with ❤️ using Streamlit, LangChain, ChromaDB, and Groq.
</p>
