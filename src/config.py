# src/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load biến môi trường từ file .env (sẽ dùng cho Database sau này)
load_dotenv()

# Định nghĩa đường dẫn gốc của dự án
# Lệnh này giúp tìm ra thư mục cha của thư mục 'src' -> chính là folder dự án
PROJECT_ROOT = Path(__file__).parent.parent 

# Đường dẫn đến thư mục data
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Tên file input
INPUT_FILE_NAME = "products.csv"
INPUT_FILE_PATH = RAW_DATA_DIR / INPUT_FILE_NAME

# DB Config (Để dành cho bước Load, cứ khai báo trước)
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "my_data_project")