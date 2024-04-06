import torch
from torchvision.models import resnet50

# Load a pre-trained ResNet50 model
model = resnet50(pretrained=True)
model.eval()  # Set the model to evaluation mode

def extract_features(image):
    with torch.no_grad():  # Inference without calculating gradients
        features = model(image.unsqueeze(0))  # Add a batch dimension
    return features
