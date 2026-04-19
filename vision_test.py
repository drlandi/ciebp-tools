import os
import json
import asyncio
import edge_tts
from google import genai
from google.genai import types
import PIL.Image

# 1. THE CONFIGURATION
API_KEY = "AIzaSyBD9LiPOjywEGrUvU2CmBlMEcPQAV6Qa_E"
client = genai.Client(api_key=API_KEY)
VOICE = "pt-BR-AntonioNeural" # The Brazilian Portuguese voice
AUDIO_OUTPUT = "lesson_audio.mp3"

# 2. THE VISION ENGINE
print("1. Loading image and booting Vision Engine...")
img = PIL.Image.open('wrench.jpg')

prompt = """
Analyze the tool in this image. You are an expert technical educator creating a guide for students. 
Return a structured JSON response strictly adhering to this format:
{
  "tool_name": "The specific name of the tool (in Portuguese)",
  "description": "A brief, clear explanation of what it is and what it is used for.",
  "safety_instructions": "Key safety rules or best practices for using it.",
  "html_snippet": "A clean, mobile-responsive HTML block containing the tool name, description, and safety instructions, formatted cleanly with basic inline CSS."
}
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, img],
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)

# 3. PARSING THE DATA
print("2. Parsing AI Data...")
raw_text = response.text
# Sometimes AI wraps JSON in markdown blocks (```json ... ```). This strips it out.
if raw_text.startswith("```json"):
    raw_text = raw_text.strip("```json").strip("```")

tool_data = json.loads(raw_text)
print(f"   -> Successfully extracted data for: {tool_data['tool_name']}")

# 4. THE AUDIO ENGINE
print("3. Booting Audio Engine...")
# Create a smooth script for the AI voice to read
spoken_script = f"Conhecendo a ferramenta: {tool_data['tool_name']}. {tool_data['description']} Atenção para as instruções de segurança: {tool_data['safety_instructions']}"

async def generate_audio():
    print(f"   -> Generating professional voiceover using {VOICE}...")
    communicate = edge_tts.Communicate(spoken_script, VOICE)
    await communicate.save(AUDIO_OUTPUT)

# Run the asynchronous audio function
asyncio.run(generate_audio())

print(f"\n✅ SUCCESS! Audio saved to your folder as '{AUDIO_OUTPUT}'")
import subprocess

# 5. THE MEDIA COMPILER (Video Generation)
print("4. Compiling Video with FFmpeg...")
VIDEO_OUTPUT = "lesson_video.mp4"

# This command loops the image, layers the audio, and stops exactly when the audio ends.
ffmpeg_cmd = [
    "ffmpeg",
    "-loop", "1",               # Loop the single image
    "-y",                       # Overwrite output file if it exists
    "-i", "wrench.jpg",         # The static background image
    "-i", AUDIO_OUTPUT,         # The AI-generated voiceover
    "-c:v", "libx264",          # Standard video codec
    "-tune", "stillimage",      # Optimizes compression for a static image
    "-c:a", "aac",              # Standard audio codec
    "-pix_fmt", "yuv420p",      # Ensures playback compatibility on all mobile devices
    "-shortest",                # Cuts the video the exact millisecond the audio stops
    VIDEO_OUTPUT
]

# Execute the command (we send stdout/stderr to DEVNULL to keep the terminal output clean)
subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"   -> Video successfully rendered as '{VIDEO_OUTPUT}'")


# 6. THE WEB EXPORTER
print("5. Exporting Web Template...")
HTML_OUTPUT = "index.html"
with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
    f.write(tool_data['html_snippet'])
print(f"   -> Web page successfully saved as '{HTML_OUTPUT}'")

print("\n🚀 PIPELINE COMPLETE! All local assets generated successfully.")
import qrcode

# 7. GERADOR DE QR CODE
print("6. Gerando o QR Code...")

# A URL exata do seu GitHub Pages
SITE_URL = "https://drlandi.github.io/ciebp-tools/"
QR_OUTPUT = "qrcode_ferramenta.png"

# Configurando o QR Code (Alta resolução e correção de erro)
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(SITE_URL)
qr.make(fit=True)

# Criando e salvando a imagem
img_qr = qr.make_image(fill_color="black", back_color="white")
img_qr.save(QR_OUTPUT)

print(f"   -> QR Code salvo com sucesso como '{QR_OUTPUT}'")
print("\n🚀 PIPELINE 100% CONCLUÍDO! O sistema está pronto.")
