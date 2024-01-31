import torch
import torch.nn as nn
from torchvision import transforms, models
from torch.utils.data import Dataset, DataLoader
import os
from PIL import Image, ImageOps
import numpy as np

# Function to pad images to the required size
def pad_to_size(img, size):
    # Padding to have square images of the required size
    old_size = img.size
    ratio = float(max(size))/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])
    img = img.resize(new_size, Image.ANTIALIAS)
    
    # Calculate padding
    delta_w = max(size[0] - new_size[0], 0)
    delta_h = max(size[1] - new_size[1], 0)
    padding = (delta_w//2, delta_h//2, delta_w - (delta_w//2), delta_h - (delta_h//2))
    img = ImageOps.expand(img, padding)
    return img

# Custom dataset class for spatial boxes
class SpatialBoxDataset(Dataset):
    def __init__(self, root_dir, size=(112, 112), frames=15):
        self.root_dir = root_dir
        self.size = size
        self.frames = frames
        self.spatial_boxes = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
        self.transform = transforms.Compose([
            transforms.Lambda(lambda img: pad_to_size(img, self.size)),
            transforms.CenterCrop(self.size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.43216, 0.394666, 0.37645], std=[0.22803, 0.22145, 0.216989])
        ])

    def __len__(self):
        return len(self.spatial_boxes)

    def __getitem__(self, idx):
        frames_data = []
        for i in range(self.frames):
            img_path = os.path.join(self.root_dir, f"b_{idx}_{i}.jpg")
            img = Image.open(img_path).convert('RGB')
            img = self.transform(img)
            frames_data.append(img)
        frames_data = torch.stack(frames_data)  # Convert to (C, T, H, W)
        return frames_data.permute(1, 0, 2, 3)  # Convert to (T, C, H, W)

# Load pre-trained r3d_18 model
pretrained_model = models.video.r3d_18(pretrained=True)
# Remove the final classification layer(s)
feature_extractor = nn.Sequential(*list(pretrained_model.children())[:-1])

# Initialize dataset and dataloader
dataset = SpatialBoxDataset(root_dir='./spatial_boxes_train')
dataloader = DataLoader(dataset, batch_size=8, shuffle=False)

# Extract features
features_list = []
for spatial_box in dataloader:
    with torch.no_grad():
        spatial_box = spatial_box.squeeze(0)  # Remove batch dimension
        features = feature_extractor(spatial_box)
        features_list.append(features.squeeze().numpy())  # Remove batch dimension and convert to numpy array

features_array = np.array(features_list)


