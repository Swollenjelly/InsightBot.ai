from flask import Flask, render_template, request, redirect, url_for, session
import os, re, yt_dlp
import assemblyai as aai
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "your-secret-key"  # required for session usage

# Load API keys
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Temporary in-memory storage (no DB)
transcript_store = {}  # { session_id: transcript_text }
chat_history = {}      # { session_id: [ {role: user/bot, content: text}, ... ] }


# ---------- YouTube Audio Download ----------
def download_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,  # 👈 show full logs
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = re.sub(r'[\\/*?:"<>|]', "", info['title'])
            print("📁 Downloaded title:", title)
            for f in os.listdir():
                print("🔍 Checking file:", f)
                if f.startswith(title) and f.endswith(".mp3"):
                    print("✅ Found:", f)
                    return f
            print("❌ No matching .mp3 file found!")
    except Exception as e:
        print("❌ Download failed:", e)
        return None

    return None


# ---------- Routes ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("index.html", error="Please enter a YouTube URL")

        audio_file = download_youtube_audio(url)
        if not audio_file:
            return render_template("index.html", error="Failed to download audio.")

        try:
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(audio_file)
            os.remove(audio_file)

            session_id = session.get("id", os.urandom(8).hex())
            session["id"] = session_id
            transcript_store[session_id] = transcript.text
            chat_history[session_id] = []

            return redirect(url_for("chat"))

        except Exception as e:
            print("❌ ERROR in transcript processing or session:", e)
            return render_template("index.html", error="Failed to process the transcript. Please try again.")


    return render_template("index.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    session_id = session.get("id")
    if not session_id or session_id not in transcript_store:
        return redirect(url_for("index"))

    if request.method == "POST":
        question = request.form.get("message")
        if question:
            chat_history[session_id].append({"role": "user", "content": question})

            prompt = f"""You are a video assistant. Use the following transcript:

{transcript_store[session_id]}

User question: {question}
"""

            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant based on a video transcript. Keep the answers casual and at times use a little hinglish from here and on"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )

            answer = response.choices[0].message.content.strip()
            chat_history[session_id].append({"role": "bot", "content": answer})

    return render_template("chat.html", messages=chat_history[session_id])


if __name__ == "__main__":
    app.run(debug=True)
