# src/main.py
import logging
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data
from src.config import INPUT_FILE_PATH

# Cấu hình log tổng
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    logging.info("=== BẮT ĐẦU DATA PIPELINE ===")
    
    # 1. Extract
    df_raw = extract_data(INPUT_FILE_PATH)
    
    if df_raw is not None:
        # 2. Transform
        df_clean = transform_data(df_raw)
        
        if df_clean is not None:
            # 3. Load
            load_data(df_clean)
            
    logging.info("=== KẾT THÚC PIPELINE ===")

if __name__ == "__main__":
    run_pipeline()