# farmers/ai_service.py
import torch
import timm
from PIL import Image
from torchvision import transforms as T
import os

# Config
MODEL_NAME = "rexnet_150"
BASE_DIR = os.path.dirname(__file__)
CHECKPOINT_PATH = os.path.join(BASE_DIR, "cabbage_best_model.pth")

# Classes (same as training order)
CLASSES = [
    "Alternaria_Leaf_Spot",
    "club root",
    "Downy Mildew",
    "Cabbage aphid colony",
    "Ring spot",
    "Black Rot",
    "Bacterial spot rot",
    "No disease",
]

# Transform
mean, std, im_size = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225], 224
tfs = T.Compose([
    T.Resize((im_size, im_size)),
    T.ToTensor(),
    T.Normalize(mean=mean, std=std)
])

# Load model once (singleton)
device = "cuda" if torch.cuda.is_available() else "cpu"
_model = timm.create_model(MODEL_NAME, pretrained=False, num_classes=len(CLASSES)).to(device)
_model.load_state_dict(torch.load(CHECKPOINT_PATH, map_location=device))
_model.eval()

def predict_one_image(image_file):
    """Predict disease from Django UploadedFile"""
    image = Image.open(image_file).convert("RGB")
    tensor = tfs(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = _model(tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        pred_idx = torch.argmax(probs, dim=1).item()
        pred_class = CLASSES[pred_idx]
        confidence = probs[0][pred_idx].item()

    return pred_class, confidence
