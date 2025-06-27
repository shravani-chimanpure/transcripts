import os
from pydub import AudioSegment
from openai import OpenAI

# Initialize Groq client
client = OpenAI(
    api_key="",
    base_url="https://api.groq.com/openai/v1"
)

mp3_file_path = "C:/Users/Admin/Desktop/Shravani/Transcripts/audio/01a - The SWE Industry.mp3"
base_filename = os.path.splitext(os.path.basename(mp3_file_path))[0]

print("🔧 Splitting audio...")
audio = AudioSegment.from_mp3(mp3_file_path)
chunk_length_ms = 10 * 60 * 1000
chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

chunk_dir = "chunks"
os.makedirs(chunk_dir, exist_ok=True)

all_text = []

for i, chunk in enumerate(chunks):
    chunk_filename = os.path.join(chunk_dir, f"{base_filename}_chunk_{i}.mp3")
    txt_filename = os.path.join(chunk_dir, f"{base_filename}_chunk_{i}.txt")

    print(f"🎧 Exporting chunk {i + 1}/{len(chunks)}...")
    chunk.export(chunk_filename, format="mp3")

    with open(chunk_filename, "rb") as audio_file:
        print(f"🧠 Transcribing chunk {i + 1}...")
        transcript = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file,
            response_format="text",
            language="en",
            temperature=0
        )

        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(transcript)

        all_text.append(transcript)

# Save full text
final_txt_path = f"{base_filename}_full_transcript.txt"
with open(final_txt_path, "w", encoding="utf-8") as f:
    f.write("\n\n".join(all_text))

print(f"✅ Done! Transcript saved to {final_txt_path}")