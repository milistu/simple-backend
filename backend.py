import os
import io
import cv2
import numpy as np
from jose import JWTError, jwt
from pydub import AudioSegment
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv, find_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import (
    FastAPI,
    UploadFile,
    HTTPException,
    Depends,
    Security,
    File,
    status,
)

from utils import load_user_db, create_access_token, verify_password

load_dotenv(find_dotenv())

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users_db = load_user_db()


# Define a Pydantic model for the payload of the token
class TokenData(BaseModel):
    username: str | None = None


def verify_token(token: str = Security(oauth2_scheme), credentials_exception=None):
    if credentials_exception is None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/upload/image/")
async def process_image(
    file: UploadFile = File(...), token: str = Depends(verify_token)
):
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
async def process_audio(
    file: UploadFile = File(...), token: str = Depends(verify_token)
):
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
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = None,
    token: str = Depends(verify_token),
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
