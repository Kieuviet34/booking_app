# Ứng Dụng Đặt Lịch Cho Quản Lý Bệnh Viện

Dự án này là một ứng dụng đặt lịch hẹn bệnh viện được xây dựng bằng Flask.

## Yêu Cầu

- Python 3.7 hoặc cao hơn
- Cơ sở dữ liệu MySQL

## Hướng Dẫn Cài Đặt

### 1. Tạo và Kích Hoạt Môi Trường Ảo

#### Trên Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

#### Trên Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Cài Đặt Các Thư Viện Phụ Thuộc
Sau khi kích hoạt môi trường ảo, cài đặt các gói cần thiết:
```bash
pip install -r requirements.txt
```

### 3. Tạo Các Bảng Cơ Sở Dữ Liệu
1. Mở MySQL và thực thi các lệnh SQL trong tệp `create_table.sql` để thiết lập các bảng cần thiết:
    ```sql
    -- Ví dụ lệnh SQL
    CREATE TABLE appointments (
         id INT AUTO_INCREMENT PRIMARY KEY,
         patient_name VARCHAR(255),
         doctor_name VARCHAR(255),
         appointment_date DATE,
         status VARCHAR(50)
    );
    ```
2. Thay đổi thông số trong app.py phần config database để kết nối

### 4. Chạy Ứng Dụng
Kích hoạt môi trường ảo (nếu chưa kích hoạt) và khởi chạy ứng dụng Flask:
```bash
python app.py
```

### 5. Truy Cập Ứng Dụng
Mở trình duyệt và truy cập:
```
http://127.0.0.1:5000/
```

## Ghi Chú
- Đảm bảo rằng MySQL đang chạy và có thể truy cập.
- Chỉnh sửa tệp `app.py` để phù hợp với thông tin đăng nhập cơ sở dữ liệu của bạn.

