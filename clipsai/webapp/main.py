from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil
import os
import subprocess

app = FastAPI(title="ClipsAI Web")

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def _is_command_available(command: str) -> bool:
	try:
		subprocess.run([command, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
		return True
	except Exception:
		return False


def _transcribe_with_clipsai(file_path: str) -> dict:
	"""Attempt to transcribe using clipsai if available. Returns a result dict."""
	try:
		from clipsai import Transcriber
		transcriber = Transcriber()
		transcription = transcriber.transcribe(file_path)
		# Concatenate sentences for a simple output
		text = transcription.text
		return {"success": True, "text": text}
	except Exception as exc:
		return {"success": False, "error": str(exc)}


@app.get("/health")
async def health() -> dict:
	return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
	ffmpeg_ok = _is_command_available("ffmpeg")
	return templates.TemplateResponse("index.html", {"request": request, "ffmpeg_ok": ffmpeg_ok})


@app.post("/upload", response_class=HTMLResponse)
async def upload(
	request: Request,
	file: UploadFile = File(...),
	action: str = Form("transcribe"),
):
	# Save uploaded file
	target_path = UPLOAD_DIR / file.filename
	with target_path.open("wb") as out_file:
		shutil.copyfileobj(file.file, out_file)

	if action == "transcribe":
		result = _transcribe_with_clipsai(str(target_path))
		if result.get("success"):
			return templates.TemplateResponse(
				"result.html",
				{"request": request, "title": "Transcription Result", "content": result.get("text", "")},
			)
		else:
			return templates.TemplateResponse(
				"error.html",
				{
					"request": request,
					"title": "Processing Error",
					"error": result.get("error", "Unknown error"),
					"hint": "Ensure dependencies like PyTorch, WhisperX, and ffmpeg are installed.",
				},
			)

	# Default: just acknowledge upload
	return templates.TemplateResponse(
		"result.html",
		{"request": request, "title": "Upload Successful", "content": f"Uploaded {file.filename}"},
	)