from modelFactory import ModelFactory
from PIL import Image

def identify(photo):
    pass

img_path = ""
model = ModelFactory.create("yolo", weights_path="model/cls_v0.0.pt")
image = Image.open(img_path).convert("RGB")
result = model.predict(image)

top_conf = result[0].probs.top1conf
top_name = result[0].names[result[0].probs.top1]

print(f'Result: {top_name} {float(top_conf):.2f}')