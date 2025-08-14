import os
import shutil
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="ClipsAI Web")

BASE_DIR = Path(os.environ.get("CLIPSAI_DATA_DIR", "/workspace/data")).resolve()
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

for d in (UPLOAD_DIR, OUTPUT_DIR):
	os.makedirs(d, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...), model_size: Optional[str] = Form(None), language: Optional[str] = Form(None)):
	filename = file.filename
	dst_path = UPLOAD_DIR / filename
	with dst_path.open("wb") as buffer:
		shutil.copyfileobj(file.file, buffer)

	return RedirectResponse(url=f"/process?filename={filename}&model_size={model_size or ''}&language={language or ''}", status_code=303)


@app.get("/process", response_class=HTMLResponse)
async def process(request: Request, filename: str, model_size: Optional[str] = None, language: Optional[str] = None):
	from clipsai import Transcriber, ClipFinder  # lazy import heavy deps

	media_path = UPLOAD_DIR / filename
	transcriber = Transcriber(model_size=model_size or None)
	transcription = transcriber.transcribe(str(media_path), iso6391_lang_code=language or None)

	clip_finder = ClipFinder()
	clips = clip_finder.find_clips(transcription)

	# Map to serializable dicts
	sentences = [s.to_dict() for s in transcription.sentences]
	words = [w.to_dict() for w in transcription.words]
	clip_dicts = []
	for c in clips:
		if hasattr(c, "to_dict"):
			clip_dicts.append(c.to_dict())
		else:
			clip_dicts.append(c)

	return templates.TemplateResponse(
		"results.html",
		{"request": request, "filename": filename, "sentences": sentences, "words": words, "clips": clip_dicts},
	)