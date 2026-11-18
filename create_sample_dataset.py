#!/usr/bin/env python3
"""
create_sample_dataset.py

Utility script to generate a synthetic NIH ChestX-ray14 mock dataset structure
with clinically distinct pathology signatures (Nodule, Effusion, Infiltration,
Cardiomegaly, and Normal lungs) for local development, CI validation, and
reproducible testing of Quantum Image Processing pipelines.

Structure generated:
dataset/
├── images/
│   ├── 00000001_000.png
│   └── ...
├── Data_Entry_2017.csv
├── train_val_list.txt
└── test_list.txt
"""

import os
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image

def generate_mock_xray(width=256, height=256, pathology="No Finding", seed=0):
    """
    Generate a realistic synthetic grayscale radiograph with simulated
    thoracic cavity, bilateral lungs, cardiac silhouette, ribs, and
    pathology-specific radiologic opacities (Nodule, Effusion, Infiltration, Cardiomegaly).
    """
    rng = np.random.RandomState(seed)
    y, x = np.mgrid[:height, :width]
    nx = (x - width / 2) / (width / 2)
    ny = (y - height / 2) / (height / 2)
    
    # Thoracic cage ellipse
    body_mask = (nx**2 / 0.85**2 + ny**2 / 0.95**2) < 1.0
    img = np.zeros((height, width), dtype=np.float32)
    img[body_mask] = 110.0
    
    # Bilateral lung radiolucency (darker regions, lower attenuation)
    left_lung = ((nx + 0.38)**2 / 0.24**2 + (ny + 0.05)**2 / 0.55**2) < 1.0
    right_lung = ((nx - 0.38)**2 / 0.24**2 + (ny + 0.05)**2 / 0.55**2) < 1.0
    img[left_lung & body_mask] = 40.0
    img[right_lung & body_mask] = 40.0
    
    # Mediastinum / spine (dense bone -> high attenuation)
    spine = (np.abs(nx) < 0.12) & body_mask
    img[spine] += 40.0
    
    # Heart silhouette: enlarged CTR in Cardiomegaly
    heart_w = 0.44 if "Cardiomegaly" in pathology else 0.28
    heart = (((nx - 0.12)**2 / heart_w**2 + (ny - 0.18)**2 / 0.28**2) < 1.0) & body_mask
    img[heart] += 38.0
    
    # Horizontal rib band variations
    ribs = 12.0 * np.sin(ny * 18.0) * body_mask
    img += ribs
    
    # Specific Clinical Pathologies
    if "Nodule" in pathology or "Mass" in pathology:
        # Dense circular radio-opacity in right lung field (image left)
        nodule_r = np.sqrt((nx + 0.35)**2 + (ny - 0.05)**2)
        nodule_mask = (nodule_r < 0.09) & body_mask
        img[nodule_mask] += 75.0 * np.exp(- (nodule_r[nodule_mask]**2) / (2 * 0.04**2))
        
    if "Effusion" in pathology:
        # Fluid meniscus pooling in costophrenic angles (bottom base of lungs)
        fluid_mask = (ny > 0.30) & (left_lung | right_lung) & body_mask
        fluid_grad = (ny - 0.30) / 0.30
        img[fluid_mask] += np.clip(fluid_grad[fluid_mask] * 70.0, 0, 70.0)
        
    if "Infiltration" in pathology:
        # Patchy irregular pneumonia consolidation in mid lung
        infiltrate_zone = (((nx + 0.35)**2 / 0.16**2 + (ny - 0.12)**2 / 0.18**2) < 1.0) & body_mask
        patchy = rng.uniform(25.0, 55.0, (height, width))
        img[infiltrate_zone] += patchy[infiltrate_zone]
        
    # Subtle stochastic detector noise
    noise = rng.normal(0, 3.5, (height, width))
    img = np.clip(img + noise, 0, 255).astype(np.uint8)
    
    return Image.fromarray(img, mode="L")

def create_dataset(dest_dir=Path("./dataset"), num_train_val=30, num_test=220):
    dest_dir = Path(dest_dir)
    images_dir = dest_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    
    total_images = num_train_val + num_test
    print(f"Generating {total_images} synthetic ChestX-ray14 images in {images_dir}...")
    
    labels_pool = [
        "No Finding",
        "Infiltration",
        "Atelectasis",
        "Effusion",
        "Nodule",
        "Pneumothorax",
        "Mass",
        "Consolidation",
        "Cardiomegaly",
        "Effusion|Infiltration",
        "Atelectasis|Effusion"
    ]
    
    metadata_rows = []
    train_val_files = []
    test_files = []
    
    for i in range(1, total_images + 1):
        filename = f"{i:08d}_000.png"
        filepath = images_dir / filename
        
        patient_id = i
        label = labels_pool[i % len(labels_pool)]
        age = 20 + (i * 3) % 65
        gender = "M" if (i % 2 == 0) else "F"
        view = "PA" if (i % 3 != 0) else "AP"
        
        # Save image with distinct clinical pathology
        img = generate_mock_xray(width=256, height=256, pathology=label, seed=i)
        img.save(filepath)
        
        metadata_rows.append({
            "Image Index": filename,
            "Finding Labels": label,
            "Follow-up #": 0,
            "Patient ID": patient_id,
            "Patient Age": age,
            "Patient Gender": gender,
            "View Position": view,
            "OriginalImage[Width": 1024,
            "Height]": 1024,
            "OriginalImagePixelSpacing[x": 0.143,
            "y]": 0.143
        })
        
        if i <= num_train_val:
            train_val_files.append(filename)
        else:
            test_files.append(filename)
            
    # Write metadata CSV
    meta_df = pd.DataFrame(metadata_rows)
    meta_csv_path = dest_dir / "Data_Entry_2017.csv"
    meta_df.to_csv(meta_csv_path, index=False)
    
    # Write split text files
    with open(dest_dir / "train_val_list.txt", "w") as f:
        f.write("\n".join(train_val_files) + "\n")
        
    with open(dest_dir / "test_list.txt", "w") as f:
        f.write("\n".join(test_files) + "\n")
        
    print(f"Sample dataset successfully created at: {dest_dir.resolve()}")
    print(f" - Images: {len(list(images_dir.glob('*.png')))}")
    print(f" - Metadata: {meta_csv_path} ({len(meta_df)} rows)")
    print(f" - Train/Val Split: {len(train_val_files)} entries")
    print(f" - Test Split: {len(test_files)} entries")

if __name__ == "__main__":
    create_dataset()
