from fastapi import FastAPI, UploadFile, File
import logging
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import os
import shutil
import base64
import io

from fastapi.responses import StreamingResponse, FileResponse




app = FastAPI()  # Create a FastAPI instance

# Configure logging
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logger = logging.getLogger()

# Add CORS middleware to handle Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()
# model = your_model_module.load_model()  # Load your model


app = FastAPI()

def predict(model_path,image_path):
    model = YOLO(model_path)
    results = model([image_path], imgsz=640, conf=0.6)
    image_filename =image_path.split("/")[-1]
    os.makedirs(PREDICTED_FOLDER, exist_ok=True)
    predicted_filename = os.path.join(PREDICTED_FOLDER,image_filename)
    logger.info(type(results))
    results[0].save(filename=predicted_filename)
    return predicted_filename
    # results.plot(save=True,filename=PREDICTED_FOLDER)


FOLDER_TO_PREDICT = "image_to_predict"
PREDICTED_FOLDER = "image_predicted"
YOLO_MODEL = "runs/detect/train_n_400_16/weights/best.pt"

# model = your_model_module.load_model()  # Load your model
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    os.makedirs(FOLDER_TO_PREDICT, exist_ok=True)
    # Save the file to a desired location
    file_path = os.path.join(FOLDER_TO_PREDICT, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    prediction_path = predict(YOLO_MODEL,file_path)
    with open(prediction_path, "rb") as pred_file:
        pred_image_content = pred_file.read()
        encoded_pred_image = base64.b64encode(pred_image_content).decode("utf-8")

    # Return the Base64 encoded predicted image as JSON response
    return {"predicted_image": encoded_pred_image}
    

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
