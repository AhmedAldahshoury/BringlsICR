from pathlib import Path
import os

# PATHS

ROOT_PATH = Path(__file__).resolve().parent
DATASET_PATH = os.path.join(ROOT_PATH, 'dataset')
GALLERY_PATH = os.path.join(ROOT_PATH, 'src', 'static', 'gallery')
TEMP_UPLOADS_PATH = os.path.join(ROOT_PATH, 'src', 'static', 'uploadsTemp')


# RECOGNITION

MIN_INSTANCES_TO_TRAIN = 10
