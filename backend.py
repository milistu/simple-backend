import io
import cv2
import numpy as np
from typing import Optional, Union
from pydub import AudioSegment
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI()


@app.post("/upload/image/")
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()
    np_contents = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_contents, cv2.IMREAD_COLOR)
    # Flip the image horizontally
    flipped_image = cv2.flip(image, 1)
    # Encode the image to bytes and send as response
    _, encoded_image = cv2.imencode(".jpg", flipped_image)
    return StreamingResponse(
        io.BytesIO(encoded_image.tobytes()), media_type="image/jpeg"
    )


@app.post("/upload/audio/")
async def process_audio(file: UploadFile = File(...)):
    contents = await file.read()

    # Determin the file format from the filename
    file_format = file.filename.split(".")[-1].lower()

    # Use BytesIO to handle the in-memory file
    audio = AudioSegment.from_file(io.BytesIO(contents), format=file_format)

    # Reverse the audio
    reversed_audio = AudioSegment.reverse(audio)

    # Export audio to bytes and send as response
    buffer = io.BytesIO()
    reversed_audio.export(buffer, format=file_format)
    buffer.seek(0)

    # Set correct content type for the response
    media_type = "audio/mpeg"  # Default to mp3
    if file_format == "wav":
        media_type = "audio/wav"
    elif file_format == "m4a":
        media_type = "audio/mp4"
    return StreamingResponse(buffer, media_type=media_type)


@app.post("/upload/text/")
async def process_text(
    file: Optional[UploadFile] = File(None), text: Optional[str] = File(None)
):
    if file:
        contents = await file.read()
        text_data = contents.decode("utf-8")
    elif text:
        text_data = text
    else:
        raise HTTPException(status_code=400, detail="No text or file provided")

    # Reverse the text
    reversed_text = text_data[::-1]
    return JSONResponse({"reverse_text": reversed_text})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
