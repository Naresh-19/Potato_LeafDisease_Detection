from fastapi import FastAPI,File,UploadFile
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import  numpy as np 
from io import BytesIO
from PIL import Image
import tensorflow as tf



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = tf.keras.models.load_model("../models/2")
CLASS_NAMES = ["Early Bright","Late Bright", "Healthy"]

@app.get("/ping")
async def ping():
  return "pong" 

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image
  
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
  image = read_file_as_image(await file.read())
  img_batch = np.expand_dims(image,0)
  
  predictions = MODEL.predict(img_batch)
  print(predictions)
  predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
  confidence = np.max(predictions[0])
  return {
      'class': predicted_class,
      'confidence': float(confidence)
  }

if __name__ == "__main__":
  uvicorn.run(app, host="localhost", port=8008)
  
  
