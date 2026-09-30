# 🎬 YouTube Content Creation Agent

An AI-powered YouTube content creation application that helps creators generate complete video content from a single topic.

The application uses **Streamlit** for the web interface, **Python** for the backend logic, and **Ollama with Llama 3.2** for local AI-powered content generation.

---

## 🚀 Features

### 🎯 YouTube Content Generation

- Generate creative YouTube video ideas
- Generate catchy video titles
- Generate YouTube descriptions
- Generate hashtags
- Generate SEO keywords
- Generate complete YouTube scripts
- Generate thumbnail concepts

### 🛠️ Advanced Content Tools

- 🎞️ Scene-by-scene video planning
- ⚡ YouTube Shorts generation
- 📱 Instagram Reel generation
- 🔄 Content repurposing
- 🔎 YouTube SEO analysis

### 📚 Content Management

- Save generated projects
- Content history
- View previous projects
- Export content as PDF
- Export content as DOCX
- Copy generated content easily

### 🖼️ Future Enhancement

- AI-generated thumbnail images using local Stable Diffusion

---

## 🧠 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Streamlit | Web application interface |
| Ollama | Local AI model runtime |
| Llama 3.2 | AI content generation |
| ReportLab | PDF generation |
| python-docx | DOCX generation |
| JSON | Content history storage |
| Git & GitHub | Version control |

---

## 🏗️ Project Architecture

```text
                    USER
                      │
                      ▼
             ┌─────────────────┐
             │  Streamlit UI   │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │  Python Agent   │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Ollama / Llama  │
             │      3.2        │
             └────────┬────────┘
                      │
             ┌────────┴────────┐
             ▼                 ▼
      YouTube Content     Social Content
             │                 │
       ┌─────┴─────┐      ┌────┴─────┐
       │           │      │          │
     Titles      Script  Shorts    Reels
     SEO         Ideas   Posts     Repurpose
     YouTube_Content_Creation_Agent/
│
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── main.py
│   ├── web_app.py
│   └── image_generator.py
│
├── data/
│   └── content_history.json
│
├── outputs/
│
├── venv/
│
├── .gitignore
├── README.md
└── requirements.txt