# src/extract.py
import pandas as pd
import logging
from src.config import INPUT_FILE_PATH

# Cấu hình log đơn giản (để in ra màn hình console cho dễ thấy)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_data(filepath):
    """
    Hàm đọc dữ liệu từ file CSV
    Input: Đường dẫn file
    Output: Pandas DataFrame hoặc None nếu lỗi
    """
    try:
        logging.info(f"Bắt đầu trích xuất dữ liệu từ: {filepath}")
        
        # Kiểm tra file có tồn tại không (dù pandas có check, nhưng mình check trước để log rõ ràng)
        if not filepath.exists():
            logging.error(f"File không tồn tại: {filepath}")
            return None

        # Đọc CSV
        # dtype=str: Mẹo nhỏ của Senior -> Đọc tất cả là chuỗi (String) trước
        # Để tránh việc Pandas tự đoán kiểu dữ liệu sai (ví dụ '001' thành 1).
        # Chúng ta sẽ ép kiểu chuẩn chỉnh ở bước Transform.
        df = pd.read_csv(filepath, dtype=str)
        
        logging.info(f"Trích xuất thành công! Kích thước: {df.shape[0]} dòng, {df.shape[1]} cột.")
        return df

    except Exception as e:
        logging.error(f"Lỗi nghiêm trọng khi Extract: {e}")
        return None

# --- ĐOẠN CODE TEST CHẠY THỬ ---
# Chỉ chạy khi run trực tiếp file này: python src/extract.py
if __name__ == "__main__":
    df = extract_data(INPUT_FILE_PATH)
    if df is not None:
        print("\n--- XEM TRƯỚC 5 DÒNG DỮ LIỆU ---")
        print(df.head())