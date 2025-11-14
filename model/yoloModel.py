from ultralytics import YOLO

from model.baseModel import BaseModel


class YOLOModel(BaseModel):
    def __init__(self, weights_path: str):
        self.model = YOLO(weights_path)

    def predict(self, image):
        results = self.model.predict(image)
        return results
