# src/scheduler.py
import schedule
import time
import logging
from src.main import run_pipeline

# Cấu hình log riêng cho Scheduler để dễ nhìn
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [SCHEDULER] - %(message)s')

def job_wrapper():
    """Hàm bọc để gọi pipeline và ghi log"""
    logging.info("⏰ ĐẾN GIỜ HOÀNG ĐẠO! Bắt đầu kích hoạt Pipeline...")
    try:
        run_pipeline()
        logging.info("✅ Pipeline chạy xong. Đang chờ lịch tiếp theo...")
    except Exception as e:
        logging.error(f"❌ Có lỗi khi chạy định kỳ: {e}")

# --- CẤU HÌNH LỊCH CHẠY ---

# 1. Chế độ TEST (Chạy mỗi 30 giây)
schedule.every(30).seconds.do(job_wrapper)

# 2. Chế độ THẬT (Chạy mỗi ngày lúc 8:00 sáng)
# schedule.every().day.at("08:00").do(job_wrapper)

# --- VÒNG LẶP VÔ TẬN ---
if __name__ == "__main__":
    logging.info("🚀 Scheduler đã khởi động. Đang chờ kích hoạt...")
    
    # In ra danh sách các lịch đang chờ
    logging.info(f"Các lịch đã đặt: {schedule.get_jobs()}")

    while True:
        # Kiểm tra xem có việc nào cần làm ngay bây giờ không?
        schedule.run_pending()
        
        # Ngủ 1 giây để đỡ tốn CPU (tránh máy tính kiểm tra liên tục quá nhanh)
        time.sleep(1)