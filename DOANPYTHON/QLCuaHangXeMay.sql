create database QLCuaHangXeMay
collate utf8mb4_unicode_ci
character set utf8mb4;

drop database QLCuaHangXeMay;
use QLCuaHangXeMay;

CREATE TABLE XeMay (
    MaXe varchar(10)  PRIMARY KEY,
    TenXe VARCHAR(100) NOT NULL,
    HangXe VARCHAR(50),
    MauXe VARCHAR(50),
    GiaXe DECIMAL(15,2),
    SoLuong INT DEFAULT 0,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DELIMITER $$
CREATE TRIGGER tg_XeMay_before_insert
BEFORE INSERT ON XeMay
FOR EACH ROW
BEGIN
    DECLARE max_id INT;

    SELECT COALESCE(MAX(CAST(SUBSTRING(MaXe, 3) AS UNSIGNED)), 0) + 1
    INTO max_id
    FROM XeMay;

    SET NEW.MaXe = CONCAT('XE', LPAD(max_id, 4, '0'));
END$$
DELIMITER ;

INSERT INTO XeMay (TenXe, HangXe, MauXe, GiaXe, SoLuong) VALUES
('Vision 2024', 'Honda', 'Đỏ', 34000000, 10),
('Sirius RC', 'Yamaha', 'Đen', 22000000, 15),
('Air Blade 160', 'Honda', 'Trắng', 52000000, 8),
('Exciter 155', 'Yamaha', 'Xanh', 47000000, 12);

CREATE TABLE LichSuGiaXe (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    MaXe VARCHAR(10),
    GiaCu DECIMAL(15,2),
    GiaMoi DECIMAL(15,2),
    NgayThayDoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (MaXe) REFERENCES XeMay(MaXe)
);
CREATE TABLE NhanVien (
    MaNV varchar(10)  PRIMARY KEY,
    HoTen VARCHAR(100) NOT NULL,
    GioiTinh ENUM('Nam','Nữ') DEFAULT 'Nam',
    NgaySinh DATE,
    SDT VARCHAR(20),
    DiaChi VARCHAR(255),
    ChucVu VARCHAR(100),
    Luong DECIMAL(15,2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DELIMITER $$
CREATE TRIGGER tg_NhanVien_before_insert
BEFORE INSERT ON NhanVien
FOR EACH ROW
BEGIN
    DECLARE max_id INT;

    SELECT COALESCE(MAX(CAST(SUBSTRING(MaNV, 3) AS UNSIGNED)), 0) + 1
    INTO max_id
    FROM NhanVien;

    SET NEW.MaNV = CONCAT('NV', LPAD(max_id, 4, '0'));
END$$
DELIMITER ;

INSERT INTO NhanVien (HoTen, GioiTinh, NgaySinh, SDT, DiaChi, ChucVu, Luong) VALUES
('Dương Hồng Ngọc', 'Nữ', '1996-05-12', '0912345678', 'An Giang', 'Quản lý', 15000000),
('Huỳnh Phú Quý', 'Nam', '2000-08-20', '0987654321', 'Cần Thơ', 'Nhân viên bán hàng', 9000000),
('Dương Hồng Quý', 'Nữ', '1994-08-01', '0901112233', 'Long Xuyên', 'Kế toán', 10000000),
('Lý Thị Thu Ngọc', 'Nữ', '1996-05-27', '0398736567', 'Đồng Tháp', 'Nhân viên bán hàng', 9000000),
('Trương Chí Khan', 'Nam', '2004-09-07', '0354255699', 'Kiêng Giang', 'Nhân viên bán hàng', 9000000);

CREATE TABLE KhachHang (
    MaKH varchar(10)  PRIMARY KEY,
    TenKH VARCHAR(100) NOT NULL,
    DiaChi VARCHAR(255),
    SDT VARCHAR(20),
    Email VARCHAR(100),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DELIMITER $$
CREATE TRIGGER tg_KhachHang_before_insert
BEFORE INSERT ON KhachHang
FOR EACH ROW
BEGIN
    DECLARE max_id INT;

    SELECT COALESCE(MAX(CAST(SUBSTRING(MaKH, 3) AS UNSIGNED)), 0) + 1
    INTO max_id
    FROM KhachHang;

    SET NEW.MaKH = CONCAT('KH', LPAD(max_id, 4, '0'));
END$$
DELIMITER ;

INSERT INTO KhachHang (TenKH, DiaChi, SDT, Email) VALUES
('Phạm Huỳnh Trúc Anh', 'Long Xuyên', '0911222333', 'anhpham@gmail.com'),
('Bùi Thị Mén', 'An Giang', '0909888777', 'maibui@gmail.com'),
('Trần Trí Tường', 'Đồng Tháp', '0977665544', 'tuongtran@gmail.com'),
('Trần Thị Trúc Giang','Cần Thơ','0989797556','giangtran@gmail.com'),
('Huỳnh Quốc Khánh','Cần Thơ','0353930698','khanhhuynh@gmail.com'),
('Nguyễn Tấn Lộc','TP HCM','0983600990','locnguyen@gmail.com');

CREATE TABLE HoaDon (
    MaHD varchar(10)  PRIMARY KEY,
    NgayBan DATE NOT NULL,
    MaKH varchar(10),
    MaNV varchar(10),
    TongTien DECIMAL(18,2) NOT NULL DEFAULT 0,
    GhiChu TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_hd_kh FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_hd_nv FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO HoaDon (NgayBan, MaHD, MaKH, MaNV, TongTien) VALUES
('2025-11-01', 'HD0002', 'KH0001', 'NV0001', 34000000),
('2025-11-02', 'HD0001', 'KH0002', 'NV0002', 52000000);

DELIMITER $$
CREATE TRIGGER tg_HoaDon_before_insert
BEFORE INSERT ON HoaDon
FOR EACH ROW
BEGIN
    DECLARE max_id INT;

    SELECT COALESCE(MAX(CAST(SUBSTRING(MaHD, 3) AS UNSIGNED)), 0) + 1
    INTO max_id
    FROM HoaDon;

    SET NEW.MaHD = CONCAT('HD', LPAD(max_id, 4, '0'));
END$$
DELIMITER ;

CREATE TABLE CTHoaDon (
    MaCT varchar(10)  PRIMARY KEY,
    MaHD varchar(10),
    MaXe varchar(10),
    SoLuong INT DEFAULT 1,
    DonGia DECIMAL(15,2),
    ThanhTien DECIMAL(15,2) GENERATED ALWAYS AS (DonGia/2) STORED,
    FOREIGN KEY (MaHD) REFERENCES HoaDon(MaHD) ON DELETE CASCADE,
    FOREIGN KEY (MaXe) REFERENCES XeMay(MaXe) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
 drop table CTHoaDon;
DELIMITER $$
CREATE TRIGGER tg_CTHoaDon_before_insert
BEFORE INSERT ON CTHoaDon
FOR EACH ROW
BEGIN
    DECLARE max_id INT;

    SELECT COALESCE(MAX(CAST(SUBSTRING(MaCT, 3) AS UNSIGNED)), 0) + 1
    INTO max_id
    FROM CTHoaDon;

    SET NEW.MaCT = CONCAT('CT', LPAD(max_id, 4, '0'));
END$$
DELIMITER ;
 
INSERT INTO CTHoaDon (MaHD, MaXe, SoLuong, DonGia) VALUES
('HD0001', 'XE0001', 1, 34000000),
('HD0002', 'XE0003', 1, 52000000);
SELECT * FROM NhanVien;
select * from TaiKhoan;
SELECT * FROM KhachHang;
SELECT * FROM XeMay;
SELECT * FROM HoaDon;
SELECT * FROM CTHoaDon;
DESCRIBE NhanVien;
describe HoaDon;


SELECT 
    hd.MaHD AS 'Mã Hóa Đơn',
    kh.TenKH AS 'Tên Khách Hàng',
    nv.HoTen AS 'Tên Nhân Viên',
    xm.TenXe AS 'Tên Xe',
    xm.HangXe AS 'Hãng Xe',
    xm.MauXe AS 'Màu Xe',
    cthd.SoLuong AS 'Số Lượng',
    cthd.DonGia AS 'Đơn Giá',
    cthd.ThanhTien AS 'Thành Tiền',
    hd.NgayBan AS 'Ngày Bán',
    hd.TongTien AS 'Tổng Tiền'
FROM HoaDon hd
JOIN KhachHang kh ON hd.MaKH = kh.MaKH
JOIN NhanVien nv ON hd.MaNV = nv.MaNV
JOIN CTHoaDon cthd ON hd.MaHD = cthd.MaHD
JOIN XeMay xm ON cthd.MaXe = xm.MaXe
ORDER BY hd.MaHD;
drop table TaiKhoan;
CREATE TABLE TaiKhoan (
    username varchar(50) PRIMARY KEY,
    password varchar(50) NOT NULL,
    role ENUM('Admin','Nhan_Vien') NOT NULL  -- 'admin' hoặc 'nhanvien'
);
INSERT INTO TaiKhoan VALUES ('admin', '0909', 'Admin');
INSERT INTO TaiKhoan VALUES ('nhanvien', '0000', 'Nhan_Vien');
select*from lichsugiaxe;
describe TaiKhoan;

