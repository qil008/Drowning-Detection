import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.transforms as transforms
from torchvision.io import read_image
from torch.utils.data import DataLoader, Dataset
import os
import numpy as np
from PIL import Image

# Define the 3D Convolutional Autoencoder architecture
class Conv3DAutoencoder(nn.Module):
    def __init__(self):
        super(Conv3DAutoencoder, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Conv3d(1, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(True),
            nn.MaxPool3d(2, stride=2),
            nn.Conv3d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(True),
            nn.MaxPool3d(2, stride=2)
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.ConvTranspose3d(128, 64, kernel_size=2, stride=2),
            nn.ReLU(True),
            nn.ConvTranspose3d(64, 1, kernel_size=2, stride=2),
            nn.Sigmoid()  # output a value between 0 and 1
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x


# Custom dataset class for loading spatial boxes
class SpatialBoxDataset(Dataset):
    def __init__(self, file_paths, transform=None):
        self.file_paths = file_paths
        self.transform = transform

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        spatial_box = []

        # Load images from a spatial box
        for file_path in self.file_paths[idx]:
            image = Image.open(file_path).convert('L')  # convert image to grayscale
            if self.transform:
                image = self.transform(image)
            spatial_box.append(image)

        # Stack images to create a '3D' spatial box
        spatial_box = torch.stack(spatial_box)

        # Add a channel dimension
        spatial_box = spatial_box.unsqueeze(0)

        return spatial_box


# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define transformations
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((64, 64)),  # resize to a fixed size
    transforms.Pad((0, 0, 0, 0)),  # may need to adjust padding
])

# Define file paths for spatial boxes (for demonstration purposes, 2 spatial boxes are defined)
spatial_boxes = [
    ['./testdata/b_1_0.jpg', './testdata/b_1_1.jpg', './testdata/b_1_2.jpg'],  # Spatial Box 1
    ['./testdata/b_2_0.jpg', './testdata/b_2_1.jpg', './testdata/b_2_2.jpg']   # Spatial Box 2
]

# Create dataset
dataset = SpatialBoxDataset(spatial_boxes, transform=transform)

# Create data loader
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

# Initialize the 3D autoencoder
model = Conv3DAutoencoder().to(device)

# Loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# Training loop
num_epochs = 10  # For demonstration, a small number of epochs; increase as needed.
for epoch in range(num_epochs):
    for spatial_box in dataloader:
        # Move tensors to the configured device
        spatial_box = spatial_box.to(device)

        # Forward pass
        outputs = model(spatial_box)
        loss = criterion(outputs, spatial_box)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Logging
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

print('Training complete')