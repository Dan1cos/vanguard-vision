from model.yoloModel import YOLOModel

model = YOLOModel("model/cls_v0.0.pt")


def predict(image):
    return model.predict(image)
