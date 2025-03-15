CREATE DATABASE booking_app;
USE booking_app;

-- Bảng users (giữ nguyên)
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,  -- Lưu mật khẩu đã băm
  phone VARCHAR(20),
  email VARCHAR(255),
  address VARCHAR(255),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng staff (thêm role và specialty)
CREATE TABLE staff (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(255) NOT NULL,
  phone VARCHAR(20),
  email VARCHAR(255),
  address VARCHAR(255),
  role VARCHAR(50) NOT NULL,  -- Ví dụ: 'doctor', 'nurse', 'assistant'
  specialty VARCHAR(50),      -- Chuyên khoa, chỉ áp dụng cho bác sĩ (ví dụ: 'noi_khoa', 'ngoai_khoa', 'san_khoa')
  status VARCHAR(50) DEFAULT 'active',  -- 'active' hoặc 'inactive'
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  is_deleted TINYINT DEFAULT 0
);

-- Bảng patients (giữ nguyên)
CREATE TABLE patients (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  phone VARCHAR(20),
  email VARCHAR(255),
  address VARCHAR(255),
  note TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  is_deleted TINYINT DEFAULT 0
);

-- Bảng appointments (thêm symptoms)
CREATE TABLE appointments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id INT NOT NULL,
  staff_id INT,  -- Có thể NULL nếu chưa xếp bác sĩ
  start_time DATETIME NOT NULL,
  end_time DATETIME NOT NULL,
  status VARCHAR(50) DEFAULT 'new',  -- 'new', 'confirmed', 'waiting', 'in_progress', 'done', 'cancelled'
  symptoms TEXT,  -- Triệu chứng của bệnh nhân (ví dụ: 'ho', 'sot', 'dau_bung')
  note TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (patient_id) REFERENCES patients(id),
  FOREIGN KEY (staff_id) REFERENCES staff(id)
);

-- Bảng work_schedules (lịch làm việc của nhân viên)
CREATE TABLE work_schedules (
  id INT AUTO_INCREMENT PRIMARY KEY,
  staff_id INT NOT NULL,
  start_time DATETIME NOT NULL,
  end_time DATETIME NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (staff_id) REFERENCES staff(id)
);

-- Bảng specialty_symptom_mapping (ánh xạ triệu chứng với chuyên khoa - tùy chọn)
CREATE TABLE specialty_symptom_mapping (
  id INT AUTO_INCREMENT PRIMARY KEY,
  specialty VARCHAR(50) NOT NULL,
  symptom VARCHAR(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng finances (giữ nguyên)
CREATE TABLE finances (
  id INT AUTO_INCREMENT PRIMARY KEY,
  transaction_date DATETIME NOT NULL,
  amount DECIMAL(12, 2) NOT NULL,
  type VARCHAR(20) NOT NULL,  -- 'income' or 'expense'
  description VARCHAR(255),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);