# src/transform.py
import pandas as pd
import logging

def clean_price(price_str):
    """
    Hàm phụ trợ: Làm sạch chuỗi giá tiền
    Input: "vnđ 500", "1500.50", NaN
    Output: 500.0, 1500.5, 0.0
    """
    if pd.isna(price_str) or price_str == '':
        return 0.0
    
    # Chuyển về string nếu chưa phải string
    price_str = str(price_str)
    
    # Chỉ giữ lại số và dấu chấm (dùng cho số thập phân)
    # Cách làm đơn giản: Thay thế tất cả ký tự KHÔNG phải số và dấu chấm thành rỗng
    clean_str = ''.join(c for c in price_str if c.isdigit() or c == '.')
    
    try:
        return float(clean_str)
    except ValueError:
        return 0.0

def transform_data(df):
    """
    Hàm xử lý chính
    """
    try:
        logging.info("Bắt đầu Transform dữ liệu...")
        
        # 1. Copy df để tránh ảnh hưởng dữ liệu gốc
        df_clean = df.copy()

        # 2. Xử lý cột Price (Áp dụng hàm clean_price cho từng dòng)
        df_clean['price'] = df_clean['price'].apply(clean_price)

        # 3. Xử lý cột ID (Chuyển sang số nguyên)
        df_clean['id'] = pd.to_numeric(df_clean['id'], errors='coerce') # coerce: lỗi thì biến thành NaN
        df_clean.dropna(subset=['id'], inplace=True) # Xóa dòng nếu ID bị lỗi (không có ID thì không nạp DB được)
        df_clean['id'] = df_clean['id'].astype(int)

        # 4. Loại bỏ dòng trùng lặp (Dựa trên ID)
        # keep='last': Giữ dòng mới nhất, 'first': Giữ dòng đầu tiên thấy.
        # Ở đây ta giả sử dòng sau cùng là mới nhất.
        initial_rows = len(df_clean)
        df_clean.drop_duplicates(subset=['id'], keep='last', inplace=True)
        dropped_rows = initial_rows - len(df_clean)
        
        if dropped_rows > 0:
            logging.warning(f"Đã loại bỏ {dropped_rows} dòng trùng lặp ID.")

        logging.info("Transform hoàn tất.")
        return df_clean

    except Exception as e:
        logging.error(f"Lỗi khi Transform: {e}")
        return None

# --- ĐOẠN CODE TEST CHẠY THỬ (Integration Test) ---
# Đoạn này sẽ giả lập quy trình: Extract -> Transform
if __name__ == "__main__":
    from src.extract import extract_data
    from src.config import INPUT_FILE_PATH
    
    # Bước 1: Extract
    raw_df = extract_data(INPUT_FILE_PATH)
    
    if raw_df is not None:
        # Bước 2: Transform
        clean_df = transform_data(raw_df)
        
        print("\n--- DỮ LIỆU SAU KHI LÀM SẠCH ---")
        print(clean_df)
        print("\n--- KIỂM TRA KIỂU DỮ LIỆU ---")
        print(clean_df.dtypes)