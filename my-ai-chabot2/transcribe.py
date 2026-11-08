import mlx_whisper
from pathlib import Path

AUDIO_FILE    = Path(__file__).with_name("recording.wav")
WHISPER_MODEL = "mlx-community/whisper-medium-mlx"
LANGUAGE      = "ko"   # None이면 Whisper가 언어를 자동 감지

def transcribe(audio_path: str, model: str = WHISPER_MODEL, language: str | None = LANGUAGE) -> str:
    """Transcribe an audio file and return the text."""
    if not Path(audio_path).is_file():
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}. Run python record.py first."
        )
    print(f"Transcribing with {model.split('/')[-1]}...")
    result = mlx_whisper.transcribe(
        str(audio_path),
        path_or_hf_repo=model,
        language=language,
    )
    return result["text"].strip()


if __name__ == "__main__":
    text = transcribe(AUDIO_FILE)
    print(f"\nTranscript:\n{text}")
