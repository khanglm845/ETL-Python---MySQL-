# src/load.py
import pandas as pd
from sqlalchemy import create_engine, text
import logging
from urllib.parse import quote_plus  # <--- CHÌA KHÓA Ở ĐÂY
from src.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

def get_db_engine():
    """Tạo connection engine đến MySQL"""
    
    # Mã hóa mật khẩu: password@  --->  password%40
    # Điều này giúp SQLAlchemy không bị nhầm lẫn dấu @
    encoded_password = quote_plus(DB_PASSWORD) 
    
    # Ghép chuỗi kết nối
    connection_str = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}"
    
    engine = create_engine(connection_str)
    return engine

def load_data(df):
    """
    Load dữ liệu vào MySQL theo chiến thuật Staging Table (Upsert)
    """
    if df is None or df.empty:
        logging.warning("Không có dữ liệu để load.")
        return

    engine = get_db_engine()
    
    try:
        logging.info("Bắt đầu quy trình Load...")
        
        # BƯỚC 1: Đẩy dữ liệu vào bảng tạm (products_staging)
        df.to_sql('products_staging', con=engine, if_exists='replace', index=False)
        logging.info("Đã đẩy dữ liệu vào bảng tạm 'products_staging'.")

        # BƯỚC 2: Thực hiện UPSERT từ Staging sang Main Table
        with engine.begin() as connection:
            sql_upsert = text("""
                INSERT INTO products (id, product_name, price, category)
                SELECT id, product_name, price, category FROM products_staging
                ON DUPLICATE KEY UPDATE
                    product_name = VALUES(product_name),
                    price = VALUES(price),
                    category = VALUES(category),
                    last_updated = CURRENT_TIMESTAMP;
            """)
            connection.execute(sql_upsert)
            
            # Dọn dẹp bảng tạm
            connection.execute(text("DROP TABLE IF EXISTS products_staging;"))
            
        logging.info("Đã đồng bộ dữ liệu sang bảng chính 'products' thành công (Upsert).")

    except Exception as e:
        logging.error(f"Lỗi nghiêm trọng khi Load: {e}")