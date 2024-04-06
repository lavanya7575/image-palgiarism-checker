from scipy.spatial.distance import cosine
import torch


def compare_images(feature_vec1, feature_vec2):
    # Flatten the feature tensors and convert to NumPy arrays if they're torch Tensors
    if isinstance(feature_vec1, torch.Tensor):
        feature_vec1 = feature_vec1.flatten().numpy()
    if isinstance(feature_vec2, torch.Tensor):
        feature_vec2 = feature_vec2.flatten().numpy()

    # Calculate cosine similarity. The closer to 1, the more similar the images are.
    similarity = 1 - cosine(feature_vec1, feature_vec2)
    return similarity
