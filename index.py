import asyncio
import edge_tts
import io
from flask import Flask, render_template, request, Response

app = Flask(__name__)
app.debug = True
# Ye line Vercel ke liye lazmi hai
app = app

VOICES = {
    "ur": "ur-PK-AsadNeural",
    "hi": "hi-IN-MadhurNeural",
    "en": "en-US-GuyNeural"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
async def convert():
    text = request.form.get('text')
    lang = request.form.get('language')
    
    if not text:
        return "Text is required", 400

    selected_voice = VOICES.get(lang, "en-US-GuyNeural")

    try:
        communicate = edge_tts.Communicate(text, selected_voice)
        audio_stream = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream.write(chunk["data"])
        
        audio_stream.seek(0)
        return Response(audio_stream.getvalue(), mimetype="audio/mpeg")

    except Exception as e:
        print(f"Error: {e}")
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
