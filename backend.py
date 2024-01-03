import os
import io
import re
import cv2
import subprocess
import numpy as np
from pydub import AudioSegment
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/upload/image/")
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()
    np_contents = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_contents, cv2.IMREAD_COLOR)
    return {"Image Size": image.shape}


@app.post("/upload/audio/")
async def process_audio(file: UploadFile = File(...)):
    contents = await file.read()

    # Use BytesIO to handle the in-memory file
    audio = AudioSegment.from_file(
        io.BytesIO(contents), format=file.filename.split(".")[-1]
    )

    # Calculate duration in milliseconds and convert to seconds
    duration_seconds = len(audio) / 1000.0

    return {"Audio Length": duration_seconds}


@app.post("/upload/text/")
async def process_text(file: UploadFile = File(...)):
    contents = await file.read()
    text = contents.decode("utf-8")
    return {"Number of Characters": len(text)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
