# ClipsAI Web App

A minimal FastAPI front-end for the ClipsAI library, supporting upload and transcription.

## Quickstart

1. Create and activate a virtual environment (recommended).
2. Install base web dependencies:

```bash
pip install -e .
```

Optional: For full transcription capabilities with GPU/CPU models, install extras (this can be heavy):

```bash
pip install -e .[full]
```

3. Run the server:

```bash
uvicorn clipsai.webapp.main:app --host 0.0.0.0 --port 8000
```

4. Open your browser at:

- http://localhost:8000/

## Notes

- ffmpeg is required for full media handling. Install via your OS package manager.
- If heavy ML dependencies are missing, the app will still run, but transcription will fail with a helpful error message.