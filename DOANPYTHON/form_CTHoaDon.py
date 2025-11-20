import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def number_to_vietnamese(n):
    units = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    tens = ["", "mười", "hai mươi", "ba mươi", "bốn mươi",
            "năm mươi", "sáu mươi", "bảy mươi", "tám mươi", "chín mươi"]
    thousands = ["", "nghìn", "triệu", "tỷ"]

    if n == 0:
        return "không"

    words = []
    i = 0

    while n > 0:
        part = n % 1000
        n //= 1000

        if part > 0:
            part_words = []
            hundred = part // 100
            ten = (part % 100) // 10
            unit = part % 10

            if hundred > 0:
                part_words.append(units[hundred] + " trăm")
            else:
                if (ten > 0 or unit > 0):
                    part_words.append("không trăm")

            if ten > 1:
                part_words.append(tens[ten])
            elif ten == 1:
                part_words.append("mười")
            else:
                if unit > 0 and hundred > 0:
                    part_words.append("lẻ")

            if unit > 0:
                if ten == 1 and unit == 5:
                    part_words.append("lăm")
                elif ten > 1 and unit == 1:
                    part_words.append("mốt")
                else:
                    part_words.append(units[unit])

            part_words.append(thousands[i])
            words.insert(0, " ".join(part_words))

        i += 1

    return " ".join(words).strip()



def open_cthd_form(root=None, conn=None, mahd=None):
    cursor = conn.cursor() if conn else None

    if root:
        root.withdraw()

    win = tk.Toplevel(root) if root else tk.Tk()
    win.title("Quản lý Chi Tiết Hóa Đơn")
    win.geometry("1250x700")
    win.configure(bg="#AEEBFF")

    # ===== CANH GIỮA =====
    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - w) // 2 - 10
    y = (sh - h) // 2 - 30
    win.geometry(f"{w}x{h}+{x}+{y}")

    # ===== TIÊU ĐỀ =====
    tk.Label(win, text="QUẢN LÝ CHI TIẾT HÓA ĐƠN",
             font=("Arial", 19, "bold"),
             fg="#003399", bg="#AEEBFF").pack(pady=10)

    temp_data = []

    # ==================== TÌM KIẾM ====================
    search_frame = tk.Frame(win, bg="#AEEBFF")
    search_frame.pack(pady=5)

    tk.Label(search_frame, text="🔍 Tìm kiếm:", font=("Arial", 11, "bold"), bg="#AEEBFF").grid(row=0, column=0, padx=5)

    search_var = tk.StringVar()
    tk.Entry(search_frame, textvariable=search_var, width=60).grid(row=0, column=1, padx=5)

    tk.Button(search_frame, text="Tìm", bg="#2196F3", fg="black", width=10,
              command=lambda: load_data(search_var.get())).grid(row=0, column=2, padx=5)

    tk.Button(search_frame, text="Tải lại", bg="#9E9E9E", fg="black", width=10,
              command=lambda: (search_var.set(""), load_data())).grid(row=0, column=3, padx=5)

    # ==================== FORM – ĐƯA LÊN TRÊN ====================
    form = tk.LabelFrame(win, text="Thông tin chi tiết hóa đơn",
                         padx=10, pady=10,
                         font=("Arial", 10, "bold"),
                         bg="#AEEBFF", fg="#003366")
    form.pack(fill="x", padx=10, pady=10)   # ⭐⭐⭐ FORM ĐƯA LÊN TRÊN

    entries = {}
    fields = ["MaHD", "MaXe", "SoLuong", "DonGia", "ThanhTien"]

    for i, field in enumerate(fields):
        tk.Label(form, text=f"{field}:", font=("Arial", 10),
                 bg="#AEEBFF").grid(row=i // 3, column=(i % 3) * 2,
                                    padx=6, pady=4, sticky="w")

        e = tk.Entry(form, width=25)
        e.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=6, pady=4)
        entries[field] = e

    entries["MaHD"].config(state="readonly")

    # ===== GIÁ GIẢM 50% =====
    tk.Label(form, text="Giá giảm 50%:", font=("Arial", 10), bg="#AEEBFF")\
        .grid(row=1, column=4, padx=6, pady=4, sticky="w")

    entry_giamgia = tk.Entry(form, width=25, state="readonly")
    entry_giamgia.grid(row=1, column=5, padx=6, pady=4)

    if mahd:
        entries["MaHD"].config(state="normal")
        entries["MaHD"].insert(0, mahd)
        entries["MaHD"].config(state="readonly")

    # ===== CLEAR FORM =====
    def clear_form():
        for f in entries:
            entries[f].config(state="normal")
            entries[f].delete(0, tk.END)

        if mahd:
            entries["MaHD"].insert(0, mahd)
            entries["MaHD"].config(state="readonly")

    # ==================== DANH SÁCH – ĐƯA XUỐNG DƯỚI ====================
    frame_list = tk.LabelFrame(win, text="Danh sách chi tiết hóa đơn",
                               padx=10, pady=10,
                               font=("Arial", 11, "bold"),
                               fg="#003366", bg="#AEEBFF")
    frame_list.pack(fill="both", expand=True, padx=10, pady=10)   # ⭐⭐⭐ LIST ĐƯA XUỐNG DƯỚI

    scroll = tk.Scrollbar(frame_list)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    columns = [
        "MaHD", "MaXe", "SoLuong", "DonGia", "ThanhTien",
        "TenKH", "TenNV", "NgayBan",
        "TenXe", "HangXe", "MauXe", "GhiChu"
    ]

    tree = ttk.Treeview(frame_list, columns=columns, show="headings",
                        yscrollcommand=scroll.set, height=12)

    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=150)

    tree.pack(fill="both", expand=True)
    scroll.config(command=tree.yview)

    # ==================== LOAD DATA ====================
    def load_data(search=None):
        tree.delete(*tree.get_children())
        temp_data.clear()

        if not cursor:
            return

        try:
            sql = """
                SELECT hd.MaHD, c.MaXe, c.SoLuong, c.DonGia, c.ThanhTien,
                       kh.TenKH, nv.HoTen, hd.NgayBan,
                       xm.TenXe, xm.HangXe, xm.MauXe, hd.GhiChu
                FROM CTHoaDon c
                JOIN HoaDon hd ON c.MaHD = hd.MaHD
                LEFT JOIN KhachHang kh ON hd.MaKH = kh.MaKH
                LEFT JOIN NhanVien nv ON hd.MaNV = nv.MaNV
                LEFT JOIN XeMay xm ON c.MaXe = xm.MaXe
            """
            params = ()

            if mahd:
                sql += " WHERE hd.MaHD=%s"
                params = (mahd,)

            if search:
                search = f"%{search}%"
                sql += " WHERE kh.TenKH LIKE %s OR xm.TenXe LIKE %s OR hd.MaHD LIKE %s"
                params = (search, search, search)

            sql += " ORDER BY hd.MaHD"
            cursor.execute(sql, params)

            for r in cursor.fetchall():
                tree.insert("", tk.END, values=r)

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    load_data()

    # ==================== LẤY GIÁ XE ====================
    def on_maxe_focus_out(event=None):
        mx = entries["MaXe"].get().strip()
        if not mx:
            return

        cursor.execute("SELECT GiaXe FROM XeMay WHERE MaXe=%s", (mx,))
        r = cursor.fetchone()

        entries["DonGia"].delete(0, tk.END)
        if r:
            entries["DonGia"].insert(0, r[0])

    entries["MaXe"].bind("<FocusOut>", on_maxe_focus_out)

    # ==================== THÊM TẠM ====================
    def add_temp():
        vals = {f: entries[f].get().strip() for f in entries}

        if not vals["MaHD"] or not vals["MaXe"]:
            messagebox.showwarning("Thiếu", "Nhập đầy đủ Mã HD và Mã Xe")
            return

        try:
            sl = int(vals["SoLuong"])
            dg = float(vals["DonGia"])
            tt = (dg / 2) * sl    # ⭐ TÍNH GIÁ GIẢM
        except:
            messagebox.showerror("Lỗi", "Số lượng hoặc đơn giá không hợp lệ!")
            return

        vals["ThanhTien"] = tt
        temp_data.append(vals)

        tree.insert("", tk.END, values=[
            vals["MaHD"], vals["MaXe"], vals["SoLuong"],
            vals["DonGia"], vals["ThanhTien"],
            "", "", "", "", "", "", ""
        ])

        clear_form()

    # ==================== SAVE ====================
    def save_all():
        if not temp_data:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để lưu.")
            return

        try:
            for ct in temp_data:
                cursor.execute("""
                    INSERT INTO CTHoaDon (MaHD, MaXe, SoLuong, DonGia)
                    VALUES (%s,%s,%s,%s)
                """, (ct["MaHD"], ct["MaXe"], ct["SoLuong"], ct["DonGia"]))

                cursor.execute("""
                    UPDATE XeMay SET SoLuong = SoLuong - %s WHERE MaXe=%s
                """, (ct["SoLuong"], ct["MaXe"]))

                cursor.execute("""
                    UPDATE HoaDon
                    SET TongTien = (SELECT SUM(ThanhTien) FROM CTHoaDon WHERE MaHD=%s)
                    WHERE MaHD=%s
                """, (ct["MaHD"], ct["MaHD"]))

            conn.commit()
            temp_data.clear()
            load_data()
            messagebox.showinfo("Thành công", "Đã lưu chi tiết hóa đơn!")

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", str(e))

    # ==================== CLICK TREEVIEW ====================
    def on_select(event):
        sel = tree.selection()
        if not sel:
            return

        row = tree.item(sel[0])["values"]

        for i, f in enumerate(fields):
            entries[f].delete(0, tk.END)
            entries[f].insert(0, row[i])

    tree.bind("<<TreeviewSelect>>", on_select)

    # ==================== IN HÓA ĐƠN ====================
    def build_invoice_text(mahd):
        cursor.execute("""
            SELECT hd.MaHD, hd.NgayBan, hd.TongTien, hd.GhiChu,
                   kh.TenKH, kh.SDT, kh.DiaChi,
                   nv.HoTen, nv.ChucVu
            FROM HoaDon hd
            LEFT JOIN KhachHang kh ON hd.MaKH = kh.MaKH
            LEFT JOIN NhanVien nv ON hd.MaNV = nv.MaNV
            WHERE hd.MaHD=%s
        """, (mahd,))
        hd = cursor.fetchone()

        cursor.execute("""
            SELECT x.MaXe, x.TenXe, x.HangXe, x.MauXe,
                   c.SoLuong, c.DonGia, c.ThanhTien
            FROM CTHoaDon c
            JOIN XeMay x ON c.MaXe = x.MaXe
            WHERE c.MaHD=%s
        """, (mahd,))
        details = cursor.fetchall()

        lines = []
        lines.append("                     CỬA HÀNG XE MÁY ")
        lines.append("               ĐC: Long Xuyên – An Giang")
        lines.append("              SĐT: 0354299556 – MST: 0123456")
        lines.append("-" * 66)

        lines.append(f"MÃ HÓA ĐƠN : {hd[0]}")
        lines.append(f"NGÀY BÁN  : {hd[1]}")
        lines.append("")

        lines.append(f"KHÁCH HÀNG: {hd[4]}")
        lines.append(f"SĐT       : {hd[5]}")
        lines.append(f"ĐỊA CHỈ   : {hd[6]}")
        lines.append("")

        lines.append(f"NHÂN VIÊN : {hd[7]}")
        lines.append("-" * 66)
        lines.append(">> THÔNG TIN SẢN PHẨM")
        lines.append("-" * 66)

        for d in details:
            lines.append(f"• Mã xe     : {d[0]}")
            lines.append(f"  Tên xe    : {d[1]}")
            lines.append(f"  Hãng      : {d[2]}")
            lines.append(f"  Màu       : {d[3]}")
            lines.append(f"  SL        : {d[4]}")
            lines.append(f"  Thành tiền: {d[6]:,} VND")
            lines.append("")

        lines.append("-" * 66)
        lines.append(f"TỔNG TIỀN : {hd[2]:,} VND")
        lines.append(f"BẰNG CHỮ : {number_to_vietnamese(int(hd[2]))} đồng")
        lines.append(f"GHI CHÚ : {hd[3] if hd[3] else 'Không có'}")
        lines.append("-" * 66)
        lines.append("          CẢM ƠN QUÝ KHÁCH – HẸN GẶP LẠI")
        lines.append("")

        return "\n".join(lines)

    def print_invoice():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chọn dòng", "Chọn 1 dòng để in hóa đơn!")
            return

        mahd_print = tree.item(sel[0])["values"][0]

        preview = tk.Toplevel(win)
        preview.title("Xem trước khi in")
        preview.geometry("700x600")

        text_box = tk.Text(preview, font=("Consolas", 11))
        text_box.pack(fill="both", expand=True)
        text_box.insert("1.0", build_invoice_text(mahd_print))
        text_box.config(state="disabled")

    # ==================== BUTTONS ====================
    btn_frame = tk.Frame(win, bg="#AEEBFF")
    btn_frame.pack()

    tk.Button(btn_frame, text="Thêm tạm", command=add_temp, width=12,
              bg="#2196F3", fg="black").grid(row=0, column=0, padx=5)

    tk.Button(btn_frame, text="Lưu", command=save_all, width=12,
              bg="#4CAF50", fg="black").grid(row=0, column=1, padx=5)

    tk.Button(btn_frame, text="Xóa", width=12,
              bg="#f44336", fg="black").grid(row=0, column=2, padx=5)

    tk.Button(btn_frame, text="Hủy", command=clear_form, width=12,
              bg="#9E9E9E", fg="black").grid(row=0, column=3, padx=5)

    tk.Button(btn_frame, text="In HĐ", command=print_invoice, width=12,
              bg="#2196F3", fg="black").grid(row=0, column=4, padx=5)

    tk.Button(btn_frame, text="Quay lại", width=12,
              bg="#2196F3", fg="black",
              command=lambda: (win.destroy(), root.deiconify() if root else None)).grid(row=0, column=5, padx=5)

    win.protocol("WM_DELETE_WINDOW",
                 lambda: (win.destroy(), root.deiconify() if root else None))



# ============== CHẠY FILE TRỰC TIẾP ==============
if __name__ == "__main__":
    from database import get_connection
    conn = get_connection()
    open_cthd_form(None, conn)
    tk.mainloop()
