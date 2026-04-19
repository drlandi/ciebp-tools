📄 Standard Operating Procedure (SOP): CIEBP Interactive Tool Pipeline
1. Objective
To automate the end-to-end creation of interactive, multimedia educational modules for laboratory equipment. The system utilizes AI vision, text-to-speech, and local media compilation to generate a fully hosted web app and a physical, scannable QR tag from a single photograph, operating entirely on a $0 budget.

2. System Environment & Prerequisites
Before initiating a new tool run, ensure the local development environment is correctly configured.

Operating System: Linux (Ubuntu/Debian)

System Dependencies: ffmpeg installed globally (sudo apt install ffmpeg).

Virtual Environment: A dedicated Python sandbox named ciebp_env.

Required Python Packages:

google-genai (For the vision/logic engine)

pillow (For image processing)

edge-tts (For the audio engine)

qrcode[pil] (For the physical tag generation)

External Access: An active, free API key from Google AI Studio and a GitHub account.

3. The Automation Workflow (Step-by-Step)
Step 1: Initialization and Preparation
Take a clear, well-lit photograph of the tool or equipment (e.g., the Anycubic printer, the CINEBP projector).

Move the image into the project directory and rename it. (Note: Update the script to point to the new filename, or temporarily rename the new image to wrench.jpg to use the existing code).

Open the terminal and activate the virtual environment:

Bash
source ciebp_env/bin/activate
Step 2: Executing the Master Pipeline
Run the orchestrator script:

python3 vision_test.py
What the system does autonomously during this step:

Phase A (Vision): Sends the image and pedagogical prompt to the Gemini API.

Phase B (Extraction): Parses the returned JSON containing the tool name, description, safety rules, and HTML code.

Phase C (Audio): Sends the generated text to Microsoft Edge's neural TTS engine to generate lesson_audio.mp3.

Phase D (Video): Triggers the local ffmpeg process to stitch the static image and the audio file into lesson_video.mp4.

Phase E (Web Export): Writes the fully formatted index.html file to the local directory.

Phase F (Routing): Generates a basic QR code linking to the designated GitHub Pages URL.

Step 3: Cloud Deployment (GitHub Pages)
Open the web browser and navigate to the target repository (e.g., github.com/drlandi/ciebp-tools).
(Best Practice for multiple tools: Create a new sub-folder in the repository for each new piece of equipment).

Upload the newly generated assets from the local machine:

index.html

lesson_video.mp4

Commit the changes. GitHub Pages will automatically rebuild and host the site within 60 to 90 seconds.

Step 4: Physical Tag Production
Once the digital infrastructure is live, generate the physical artifact.

Open gerar_tag.py and update the configuration variables at the top of the file:

URL (The specific GitHub Pages link for this tool)

TITULO (e.g., "CIEBP Zuleika")

PERGUNTA (e.g., "Quem Sou eu???")

FERRAMENTA (The specific name of the tool)

Run the tag generator:

Bash
python3 gerar_tag.py
Open the resulting tag_impressao.png file, print it on high-quality paper, laminate it, and attach it to the equipment using a zip tie through the designated hole punch area.

4. Maintenance & Troubleshooting Notes
API Key Rotation: If the script throws an authentication error, generate a new key in Google AI Studio and update the API_KEY variable in vision_test.py.

Library Deprecation: The AI landscape moves quickly. If google-genai throws a FutureWarning or 404 error, check for package updates via pip.

HTML Video Tag: Ensure the html_snippet instruction within the Gemini prompt explicitly commands the inclusion of the <video> tag for lesson_video.mp4.
