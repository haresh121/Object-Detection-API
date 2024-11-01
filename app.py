from flask import Flask, jsonify, request, send_from_directory
from PIL import Image
from ultralytics import YOLO
import secrets, requests
from io import BytesIO
import numpy as np
from time import process_time

app = Flask(__name__)


model = YOLO("./yolo11m.pt", task="object-detection")

names = model.names.copy()


@app.get("/health")
def test():
    return jsonify({"status": "Working"})


@app.post("/segment/")
def process_image():
    start_time = process_time()
    try:
        data = request.get_json()
        im_path = data["path"]
        req = requests.get(im_path)
    
        img = Image.open(BytesIO(req.content)).convert("RGB")
        img = np.array(img)[:, :, ::-1].copy()
    
        result = model(img)[0]
    
        classes = {}
    
        for _cls in result.boxes.cls:
            if names[int(_cls)] in classes:
                classes[names[int(_cls)]] += 1
            else:
                classes[names[int(_cls)]] = 1
    
        filename = secrets.token_urlsafe(8)
    
        result.save(f"static/{filename}.png")
    except Exception as e:
        return jsonify(status_code=500, info="Internal Server Error", e=e)
    
    stop_time = process_time()

    time = stop_time - start_time
    
    return jsonify(
        info=f"saved as {filename}.ong, please go to the /static/{filename}.png link to access the detections",
        classes=classes,
        time=time,
    )


@app.get("/static/<path:path>")
def get_file(path):
    return send_from_directory("./static", path)


if __name__ == "__main__":
    app.run("localhost", 4038)
