from yoloModel import YOLOModel

class ModelFactory():
    @staticmethod
    def create(model_type: str, **kwargs):
        if model_type == "yolo":
            return YOLOModel(**kwargs)
        else:
            return YOLOModel(**kwargs)