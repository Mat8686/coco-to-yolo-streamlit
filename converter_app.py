"""
   ____      _           _        _         _         _             
  / ___|___ | | ___  ___| |_ __ _| |__  ___| |__  ___| |_ ___  _ __ 
 | |   / _ \| |/ _ \/ __| __/ _` | '_ \/ __| '_ \/ __| __/ _ \| '__|
 | |__| (_) | |  __/ (__| || (_| | |_) \__ \ | | \__ \ || (_) | |   
  \____\___/|_|\___|\___|\__\__,_|_.__/|___/_| |_|___/\__\___/|_|   
                                                                     
COCO to YOLO Converter UI
A simple Streamlit web app to convert COCO annotation files (JSON) to YOLO format label files.

Author: Matti Akbari
GitHub: https://github.com/Mat8686
LinkedIn: https://www.linkedin.com/in/mattiakbari/
License: MIT

2024
"""

# --- rest of your code below ---
import streamlit as st
import json
import os
import zipfile
from datetime import datetime

def convert_coco_to_yolo(coco_json, output_dir, normalize=True):
    images = {img['id']: img for img in coco_json['images']}
    for ann in coco_json['annotations']:
        image = images[ann['image_id']]
        img_w, img_h = image['width'], image['height']
        bbox = ann['bbox']  # [x_min, y_min, width, height]

        if normalize:
            x_center = (bbox[0] + bbox[2] / 2) / img_w
            y_center = (bbox[1] + bbox[3] / 2) / img_h
            width = bbox[2] / img_w
            height = bbox[3] / img_h
        else:
            x_center = bbox[0]
            y_center = bbox[1]
            width = bbox[2]
            height = bbox[3]
        class_id = ann['category_id'] - 1  # YOLO expects 0-based class IDs

        base_name = os.path.splitext(os.path.basename(image['file_name']))[0]
        label_path = os.path.join(output_dir, f"{base_name}.txt")
        with open(label_path, 'a') as f:
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

def main():
    st.set_page_config(page_title="COCO to YOLO Converter", page_icon="🔄", layout="centered")
    st.title("🔄 COCO to YOLO Converter")
    st.markdown("Upload a COCO annotation file (JSON) and download YOLO-format labels for all images.")

    uploaded_file = st.file_uploader("Choose a COCO annotation file", type=["json"])

    normalize = st.radio(
        "How should bbox values be handled?",
        ["Normalize bbox values (standard YOLO)", "Use bbox values as-is (already normalized)"]
    ) == "Normalize bbox values (standard YOLO)"

    if uploaded_file is not None:
        try:
            coco_data = json.load(uploaded_file)
            st.success("✅ File loaded successfully!")

            # Prepare output directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = os.path.join("download", f"yolo_labels_{timestamp}")
            os.makedirs(output_dir, exist_ok=True)

            # Convert and save YOLO labels
            convert_coco_to_yolo(coco_data, output_dir, normalize=normalize)
            st.success(f"✅ Converted to YOLO format! Saved {len(os.listdir(output_dir))} label files.")

            # Zip the output folder for download
            zip_path = f"{output_dir}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(output_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, output_dir)
                        zipf.write(file_path, arcname)

            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📥 Download YOLO Labels (ZIP)",
                    data=f,
                    file_name=os.path.basename(zip_path),
                    mime="application/zip"
                )

            st.info(f"All YOLO .txt files are inside the ZIP archive. Each file is named after the image.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.exception(e)

if __name__ == "__main__":
    main() 