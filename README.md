# 🎙️ AI Meeting Intelligence Assistant with RAG

An AI-powered Meeting Intelligence Assistant that converts meeting recordings into actionable insights using **Automatic Speech Recognition (ASR)**, **Large Language Models (LLMs)**, and **Retrieval-Augmented Generation (RAG)**.

The application supports both **English** and **Hindi/Hinglish** meetings, automatically generates summaries, extracts action items, key decisions, open questions, and allows users to chat with meeting transcripts using semantic search.

---

## 🚀 Live Demo

🌐 **Streamlit App:**  
https://ml-cdac-project-xd26cbuwfuegqqkojuwp8w.streamlit.app/

---

## 📌 Features

- 🎤 Upload audio/video files or provide a YouTube meeting URL
- 🌍 Supports:
  - English (OpenAI Whisper)
  - Hindi & Hinglish (Sarvam AI)
- 📝 Automatic meeting transcription
- 📄 AI-generated meeting summary
- ✅ Extract Action Items
- 📌 Extract Key Decisions
- ❓ Extract Open Questions & Follow-ups
- 💬 Chat with Meeting using Retrieval-Augmented Generation (RAG)
- 🔍 Semantic Search using ChromaDB
- 📥 Export meeting report as PDF
- 🌐 Interactive Streamlit Web Interface

---

# 🏗️ Project Architecture

```
                Audio File / YouTube URL
                          │
                          ▼
                Audio Processing Module
                          │
                          ▼
          Whisper / Sarvam Speech Recognition
                          │
                          ▼
                   Meeting Transcript
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
  Meeting Summary   Action Items    Key Decisions
                                          │
                                          ▼
                              Open Questions
                                          │
                                          ▼
                               Build Vector Store
                                          │
                                          ▼
                                    ChromaDB
                                          │
                                          ▼
                                   RAG Retriever
                                          │
                                          ▼
                                  Mistral LLM
                                          │
                                          ▼
                              Interactive Q&A Chat
```

---

# 📂 Project Structure

```
ML-CDAC-Project/
│
├── app.py                     # Streamlit Application
├── requirements.txt
├── README.md
├── .env
│
├── core/
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── extractor.py
│   ├── rag_engine.py
│   └── vector_store.py
│
├── utils/
│   └── audio_processor.py
│
├── reports/
├── vector_db/
├── uploads/
└── downloads/
```

---

# 🛠️ Tech Stack

## Programming Language

- Python 3.12

## Frontend

- Streamlit

## Speech Recognition

- OpenAI Whisper
- Sarvam AI

## Large Language Model

- Mistral AI

## RAG Components

- LangChain
- ChromaDB
- HuggingFace Embeddings (BGE)

## Audio Processing

- Pydub
- FFmpeg
- yt-dlp

## PDF Generation

- ReportLab

---

# ⚙️ How It Works

### Step 1

Upload

- Audio File
- Video File
- YouTube URL

↓

### Step 2

Audio is converted into WAV format and split into chunks.

↓

### Step 3

Speech is converted into text.

- Whisper → English
- Sarvam AI → Hindi/Hinglish

↓

### Step 4

Transcript is generated.

↓

### Step 5

Mistral LLM generates

- Summary
- Action Items
- Key Decisions
- Open Questions

↓

### Step 6

Transcript is embedded and stored in ChromaDB.

↓

### Step 7

Users can ask questions about the meeting using RAG.

---

# 📷 Application Screenshots

> Add screenshots here after uploading images to GitHub.

Example:

```
images/
    home.png
    summary.png
    chat.png
```

Then include:

```markdown
![Home](images/home.png)

![Summary](images/summary.png)

![Chat](images/chat.png)
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/ML-CDAC-Project.git

cd ML-CDAC-Project
```

---

## Create Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

```env
MISTRAL_API_KEY=your_mistral_api_key

SARVAM_API_KEY=your_sarvam_api_key
```

---

## Run Application

```bash
streamlit run app.py
```

---

# 📊 Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Backend |
| Streamlit | Web Application |
| Whisper | English Speech Recognition |
| Sarvam AI | Hindi Speech Recognition |
| Mistral AI | LLM |
| LangChain | LLM Framework |
| ChromaDB | Vector Database |
| HuggingFace Embeddings | Text Embeddings |
| Pydub | Audio Processing |
| FFmpeg | Audio Conversion |
| ReportLab | PDF Generation |

---

# 🎯 Future Enhancements

- Multi-language support
- Speaker diarization
- Meeting sentiment analysis
- Calendar integration
- Email meeting summary
- Cloud storage integration
- Real-time meeting transcription
- AI Agent-based workflow automation

---

# 👨‍💻 Author

**Prathamesh Ravindra Garate**

CDAC DBDA Project

---

# ⭐ If you like this project

Please consider giving this repository a ⭐ on GitHub.

---