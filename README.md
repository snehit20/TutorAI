TutorAI 📚🤖

TutorAI is an AI-powered study assistant that allows you to chat with your PDFs while optionally enhancing answers with real-time web search. It builds a searchable knowledge base from your uploaded documents and provides context-aware, conversational responses using modern LLMs.

✨ Features
📄 Upload one or more PDF documents
💬 Chat naturally with your notes
🌐 Optional web search using Tavily for additional context
🧠 Prioritizes information from your uploaded notes over web sources
🔍 Semantic search with ChromaDB + FAISS
📝 Conversation memory for follow-up questions
⚡ Powered by Groq's Llama 3.3 70B model
🎨 Clean and interactive Streamlit interface
🛠️ Tech Stack
Category	Technologies
Frontend	Streamlit
LLM	Groq (Llama 3.3 70B)
Framework	LangChain
Embeddings	HuggingFace (all-MiniLM-L6-v2)
Vector Database	ChromaDB
Retrieval	FAISS
Web Search	Tavily Search API
PDF Processing	PyPDF, PyPDFLoader
📂 Project Structure
TutorAI/
│
├── Data/                  # Uploaded PDFs
├── db/                    # Vector database
├── app.py                 # Streamlit UI
├── sample.py              # RAG pipeline
├── requirements.txt
├── .gitignore
└── README.md
⚙️ Installation

Clone the repository:

git clone https://github.com/snehit20/TutorAI.git
cd TutorAI

Create a virtual environment:

python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Linux/macOS

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt
🔑 Environment Variables

Create a .env file in the project root.

GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key

If you're deploying on Streamlit Community Cloud, add these keys under App Settings → Secrets instead.

▶️ Running the Application
streamlit run app.py
🚀 How It Works
Upload one or more PDF files.
(Optional) Enter a topic to retrieve supporting web information.
Build the knowledge base.
Ask questions in natural language.
TutorAI retrieves the most relevant context and generates answers while prioritizing your uploaded notes.
📸 Demo

Live Demo: https://YOUR-STREAMLIT-APP.streamlit.app

(Replace with your deployed Streamlit link.)

🔮 Future Improvements
Support for DOCX, PPTX, and TXT files
Source citations in responses
Multi-user authentication
Persistent chat history
Export conversations
Image and table understanding
Streaming citations with answers
🤝 Contributing

Contributions, ideas, and suggestions are always welcome.

If you find a bug or have a feature request, feel free to open an issue or submit a pull request.

📬 Contact

Snehit Singh

LinkedIn: (Add your LinkedIn profile)
GitHub: https://github.com/snehit20

⭐ If you found this project interesting, consider giving it a star on GitHub!
