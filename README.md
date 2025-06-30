# InsightBot.ai

InsightBot.ai is a Flask-based web application that allows users to interact with YouTube video transcripts via an AI chatbot. Users provide a YouTube URL, and InsightBot.ai handles audio extraction, transcription, and AI-powered Q\&A in a chat-like interface.

## Features

✅ Download and process YouTube audio
✅ Transcribe audio using AssemblyAI
✅ Ask questions about the transcript via an OpenAI-powered chatbot
✅ Stores chat history in JSON file
✅ Responsive, modern UI with Tailwind CSS

---

## Tech Stack

* **Backend:** Python (Flask)
* **Frontend:** HTML, Tailwind CSS
* **APIs:** AssemblyAI (speech-to-text), OpenAI (chat completion)
* **Tools:** yt-dlp for YouTube audio download

---

## Installation

### 1️⃣ Clone the repo

```bash
git clone https://github.com/your-username/InsightBot.ai.git
cd InsightBot.ai
```

### 2️⃣ Set up environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3️⃣ Add API keys

Create a `.env` file in the root directory:

```env
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
OPENAI_API_KEY=your_openai_api_key
```

### 4️⃣ Run the app

```bash
python app.py
```

The app will start at: [http://localhost:5000](http://localhost:5000)

---

## Project structure

```
InsightBot.ai/
├── app.py                # Main Flask app
├── chat.html              # Chat UI template
├── requirements.txt       # Python dependencies
├── .gitignore             # Ignored files
├── chat_history.json       # Chat log (auto-generated)
├── static/
│   └── img/
│       └── logo.png       # App logo
└── templates/
    └── index.html         # Home page template (not included in uploads)
```

---

## How it works

1️⃣ User submits a YouTube link
2️⃣ App downloads audio using `yt_dlp`
3️⃣ Audio is transcribed with AssemblyAI
4️⃣ Transcript is stored, chat opens
5️⃣ User can chat with AI about the video content

---

## Notes

* This app currently stores chat history in `chat_history.json`. Consider upgrading to a database for production.
* Requires `FFmpeg` installed locally for yt-dlp audio extraction.
* You can use `cookies.txt` for downloading age-restricted/private videos.

---

## License

MIT License (or insert your preferred license)

---

