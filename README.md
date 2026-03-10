# Badge Detection Dataset

YOLO dataset for training a model to detect name badges on people. Used with the PPE Compliance Monitor application.

## Folder Structure

```
badges/
├── images/
│   ├── train/          # Training images (people with/without badges)
│   └── val/            # Validation images (held-out set for evaluation)
├── labels/
│   ├── train/          # Label files (.txt) for training images
│   └── val/            # Label files (.txt) for validation images
├── data/
│   └── predefined_classes.txt   # Class list for Label Studio / LabelImg
├── badge-data.yaml     # Dataset config for Ultralytics YOLO
└── README.md
```

## Folder Purposes

| Folder | Purpose |
|--------|---------|
| `images/train` | Images used to train the model. Include both positive examples (people with badges) and negative examples (people without badges). |
| `images/val` | Images used to validate the model during training. Not used for weight updates; used to select the best checkpoint and detect overfitting. |
| `labels/train` | YOLO-format label files for each training image. One `.txt` per image, same base filename. |
| `labels/val` | YOLO-format label files for each validation image. Empty `.txt` for images with no badges. |
| `data/` | Optional. `predefined_classes.txt` lists class names for labeling tools (e.g., Label Studio, LabelImg). |
| `badge-data.yaml` | Dataset configuration. Tells Ultralytics where images and labels are and how classes are named. |

## Label Format

Each `.txt` file uses YOLO format: one line per object.

```
class_id  x_center  y_center  width  height
```

All coordinates are normalized (0–1). Example:

```
0  0.343122  0.721636  0.260756  0.105541
```

- `0` = Badge
- `0.343122` = horizontal center (34.3% from left)
- `0.721636` = vertical center (72.2% from top)
- `0.260756` = width (26.1% of image width)
- `0.105541` = height (10.6% of image height)

Images with no badges use an empty `.txt` file.

## Training

### Prerequisites

```bash
pip install ultralytics
```

### Command

From any directory:

```bash
yolo detect train \
  data=/home/gmurthy/Pictures/badges/badge-data.yaml \
  model=yolov8n.pt \
  epochs=100 \
  imgsz=640 \
  name=badge-demo
```

Or from Python:

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.train(
    data="/home/gmurthy/Pictures/badges/badge-data.yaml",
    epochs=100,
    imgsz=640,
    name="badge-demo",
)
```

### Training Output

Training writes to `runs/detect/badge-demo/` (relative to the current working directory):

| Path | Description |
|------|-------------|
| `weights/best.pt` | Best checkpoint by validation metrics. Use this for inference and deployment. |
| `weights/last.pt` | Checkpoint from the final epoch. |
| `results.png` | Plots of loss and metrics over epochs. |
| `results.csv` | Per-epoch metrics (loss, mAP, etc.). |
| `confusion_matrix.png` | Confusion matrix (if validation has labels). |

Console output includes:

- **Epoch progress** – Loss and metrics per epoch
- **Validation** – mAP50, mAP50-95, precision, recall
- **Speed** – Preprocess, inference, and postprocess times

### Export to OpenVINO (for PPE app)

```bash
yolo export model=runs/detect/badge-demo/weights/best.pt format=openvino task=detect
```

## Labeling Tools

- **Label Studio** – https://labelstud.io (self-hosted or cloud)
- **Makesense.ai** – https://www.makesense.ai (browser-based)
- **LabelImg** – Desktop app (requires Python 3.10/3.11; issues on 3.13)

Export in **YOLO** format and copy `.txt` files into `labels/train/` and `labels/val/`.
