"""
whisper-stt.py — Transcripción de audio con Whisper local
Banorte Claw (Yara) · faster-whisper tiny · CPU · int8

Uso:
  python3 whisper-stt.py <archivo_audio>

Salida:
  Texto transcrito en stdout
"""

import sys
import os

os.environ["HF_HOME"] = "/home/node/.openclaw/workspace/.cache/huggingface"

from faster_whisper import WhisperModel

def transcribe(audio_path: str) -> str:
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, beam_size=5)
    text = " ".join(seg.text.strip() for seg in segments)
    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 whisper-stt.py <archivo_audio>")
        sys.exit(1)
    path = sys.argv[1]
    print(f"🎙️ Transcribiendo: {path}")
    result = transcribe(path)
    print(f"\n📝 Transcripción:\n{result}")
