from fastapi import FastAPI, UploadFile, File
from gradio_client import Client, handle_file

app = FastAPI()

client = Client("dj-dawgs-ipd/IPD_IMAGE_PIPELINE")

@app.post("/predict-image/")
async def predict_image(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = client.predict(
        image=handle_file(temp_file_path),
        api_name="/predict"
    )

    return {"prediction": result}