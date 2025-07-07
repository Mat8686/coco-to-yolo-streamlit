# COCO to YOLO Converter UI

```
   ____      _           _        _         _         _             
  / ___|___ | | ___  ___| |_ __ _| |__  ___| |__  ___| |_ ___  _ __ 
 | |   / _ \| |/ _ \/ __| __/ _` | '_ \/ __| '_ \/ __| __/ _ \| '__|
 | |__| (_) | |  __/ (__| || (_| | |_) \__ \ | | \__ \ || (_) | |   
  \____\___/|_|\___|\___|\__\__,_|_.__/|___/_| |_|___/\__\___/|_|   
```

A simple Streamlit web app to convert COCO annotation files (JSON) to YOLO format label files.

**Author:** [Matti Akbari](https://www.linkedin.com/in/mattiakbari/)
**GitHub:** [Mat8686](https://github.com/Mat8686)
**License:** MIT

---

## Features
- Upload a COCO annotation file (JSON)
- Converts all bounding boxes to YOLO format
- Download all YOLO .txt label files as a ZIP archive
- Option to output normalized (standard YOLO) or as-is (already normalized) bbox values

## How it works
1. **Upload** your COCO annotation file (JSON format)
2. Choose how bbox values should be handled:
   - Normalize bbox values (standard YOLO): Converts pixel coordinates to normalized [0,1] values
   - Use bbox values as-is (already normalized): Outputs the bbox values exactly as they are in the COCO file
3. The app converts each annotation:
   - COCO bbox: `[x_min, y_min, width, height]`
   - YOLO bbox: `[class_id, x_center, y_center, width, height]`
   - `class_id` is 0-based (COCO is 1-based, so we subtract 1)
   - Each image gets a `.txt` file with all its objects
4. **Download** the ZIP archive containing all YOLO label files

## Usage
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run converter_app.py
   ```
3. Use the web UI to upload your COCO file, select normalization mode, and download the YOLO labels.

## Output
- Each image gets a `.txt` file named after the image (slashes replaced with `--`)
- Each line in the file: `class_id x_center y_center width height`
- All label files are zipped for easy download

## Notes
- Only bounding boxes are converted (segmentation/polygon data is ignored)
- Make sure your COCO file has `images`, `annotations`, and `categories` keys
- The app does not move or rename your image files, only creates YOLO label files 