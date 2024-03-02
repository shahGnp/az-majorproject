from typing import Union

from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
from random import randint
import uuid

app = FastAPI()

IMAGEDIR='.'

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
 
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
 
    #save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    
    print('File received and saved', file.filename)
    return {"filename": file.filename}

@app.get("/cat", responses={200: {"description": "A picture of a cat.", "content" : {"image/jpeg" : {"example" : "No example available. Just imagine a picture of a cat."}}}})
def cat():
    file_path = './detecton.png'
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/jpeg", filename="mycat.png")
    return {"error" : "File not found!"}

@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    file.filename = f"{uuid.uuid4()}.png"
    contents = await file.read()

    # Save the file
    with open(f"{IMAGEDIR}/{file.filename}", "wb") as f:
        f.write(contents)

    print('File received and saved:', file.filename)

    # Process the image (e.g., resize)
    processed_image_filename = f"{uuid.uuid4()}_processed.png"
    with Image.open(f"{IMAGEDIR}/{file.filename}") as img:
        processed_img = img.resize((300, 300))  # Example: Resize to 300x300

        # Save the processed image
        processed_img.save(f"{IMAGEDIR}/{processed_image_filename}")

    print('Image processed and saved:', processed_image_filename)

    # Return the processed image
    return FileResponse(f"{IMAGEDIR}/{processed_image_filename}", media_type="image/png", filename=processed_image_filename)