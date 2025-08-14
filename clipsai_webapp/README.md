# ClipsAI Web

A minimal FastAPI web UI around the `clipsai` library for uploading audio/video, transcribing with WhisperX, and auto-finding clips.

## Requirements
- Python 3.10+
- ffmpeg installed and available in PATH
- GPU optional; CPU will use smaller model by default

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r clipsai_webapp/requirements.txt
pip install -e .  # install local clipsai package
```

## Run (local Python)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r clipsai_webapp/requirements.txt
pip install -e .
uvicorn clipsai_webapp.app.main:app --reload --host 0.0.0.0 --port 8000
```

## Run (Docker)
```bash
cd clipsai_webapp
DOCKER_BUILDKIT=1 docker build -t clipsai-web -f Dockerfile ..
docker run --rm -it -p 8000:8000 -e CLIPSAI_DATA_DIR=/data -v clipsai-data:/data clipsai-web
```
Then open http://localhost:8000

## Notes
- Set `CLIPSAI_DATA_DIR` to change storage location (uploads/outputs).
- First run will download models (WhisperX and sentence-transformers).