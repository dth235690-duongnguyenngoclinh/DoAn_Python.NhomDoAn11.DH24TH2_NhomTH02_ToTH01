import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from form_KhachHang import open_kh_form
from form_CTHoaDon import open_cthd_form

def open_hd_form(root=None, conn=None):
    is_standalone = False
    if root is None:
        is_standalone = True
        root = tk.Tk()
        root.withdraw()
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    win = tk.Toplevel(root)
    win.title("Quản lý Hóa đơn")
    win.geometry("1000x600")
    win.configure(bg="#AEEBFF")   # ⭐ NỀN XANH
    if root is not None:
        root.withdraw()
    # ===== TIÊU ĐỀ =====
    tk.Label(
        win,
        text="QUẢN LÝ HÓA ĐƠN",
        font=("Arial", 19, "bold"),
        fg="#003399",
        bg="#AEEBFF"
    ).pack(pady=10)
    # ===== THANH TÌM KIẾM =====
    search_frame = tk.Frame(win, bg="#AEEBFF")
    search_frame.pack(pady=5)
    tk.Label(
        search_frame,
        text="🔍 Tìm kiếm:",
        font=("Arial", 11, "bold"),
        bg="#AEEBFF"
    ).grid(row=0, column=0, padx=5)
    search_var = tk.StringVar()
    tk.Entry(
        search_frame, textvariable=search_var,
        width=60, font=("Arial", 10)
    ).grid(row=0, column=1, padx=5)
    tk.Button(search_frame, text="Tìm",bg="#2196F3", fg="black", width=10,command=lambda: load_data(search_var.get())).grid(row=0, column=2, padx=5)
    tk.Button(search_frame, text="Tải lại",bg="#9E9E9E", fg="black", width=10,command=lambda: (search_var.set(""), load_data())).grid(row=0, column=3, padx=5)
    # ===== DANH SÁCH HÓA ĐƠN =====
    frame_dshd = tk.LabelFrame(
        win,
        text="Danh sách hóa đơn",
        padx=5, pady=1,
        font=("Arial", 11, "bold"),
        fg="#003366",
        bg="#AEEBFF"
    )
    frame_dshd.pack(padx=5, pady=1, fill="both", expand=True)
    scroll = tk.Scrollbar(frame_dshd)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    columns = ["MaHD", "TenKH", "TenNV", "TongTien", "NgayBan"]
    tree = ttk.Treeview(
        frame_dshd,
        columns=columns,
        show="headings",
        yscrollcommand=scroll.set,
        height=10
    )
    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=150)

    tree.pack(fill="both", expand=True)
    scroll.config(command=tree.yview)
    # ===== FORM =====
    form = tk.LabelFrame(
        win,
        text="Thông tin hóa đơn",
        padx=10, pady=10,
        font=("Arial", 10, "bold"),
        bg="#AEEBFF",
        fg="#003366"
    )
    form.pack(pady=10, padx=10, fill="x")
    entries = {}
    left_fields = ["MaHD", "NgayBan", "MaNV"]
    for i, c in enumerate(left_fields):
        tk.Label(
            form,
            text=c + ":",
            font=("Arial", 10),
            bg="#AEEBFF"
        ).grid(row=i, column=0, sticky="w", padx=6, pady=4)

        e = tk.Entry(form, width=30)
        e.grid(row=i, column=1, padx=6, pady=4)
        entries[c] = e

    entries["MaHD"].config(state="readonly")
    # --- Khách hàng ---
    tk.Label(
        form,
        text="Khách hàng:",
        font=("Arial", 10),
        bg="#AEEBFF"
    ).grid(row=3, column=0, sticky="w", padx=6, pady=4)
    kh_var = tk.StringVar()
    cb_kh = ttk.Combobox(form, textvariable=kh_var, width=33)
    cb_kh.grid(row=3, column=1, padx=6, pady=4)
    entries["MaKH"] = cb_kh
    tk.Button(
        form, text="🔍 Tìm khách", width=12,
        bg="#2196F3", fg="black",
        command=lambda: search_customer()
    ).grid(row=3, column=3, padx=5)
    tk.Button(
        form, text="➕ Thêm khách", width=12,
        bg="#4CAF50", fg="black",
        command=lambda: add_customer_and_reload()
    ).grid(row=3, column=4, padx=5)
    # ===== TỔNG TIỀN (NHƯ CODE CŨ: CHỈ TẠO LABEL NHƯNG KHÔNG GRID) =====
    tongtien_var = tk.StringVar()
    lbl_tongtien = tk.Label(
        form,
        textvariable=tongtien_var,
        font=("Arial", 10),
        bg="#f0f0f0",
        width=28,
        anchor="w"
    )
    tk.Label(
        form, text="GhiChu:", font=("Arial", 10),
        bg="#AEEBFF"
    ).grid(row=5, column=0, sticky="w", padx=6, pady=4)
    ghi = tk.Entry(form, width=30)
    ghi.grid(row=5, column=1, padx=6, pady=4)
    entries["GhiChu"] = ghi

    temp_data = []
    def next_mahd():
        entries["MaHD"].config(state="normal")
        entries["MaHD"].delete(0, tk.END)
        entries["MaHD"].insert(0, "Auto (DB)")
        entries["MaHD"].config(state="readonly")

    def load_customers():
        cursor.execute("SELECT MaKH, TenKH, SDT FROM KhachHang ORDER BY MaKH ASC")
        rows = cursor.fetchall()
        cb_kh['values'] = [f"{r[0]} - {r[1]} ({r[2]})" for r in rows]

    def search_customer():
        kw = kh_var.get().strip()
        if not kw:
            return
        cursor.execute("""
            SELECT MaKH, TenKH, SDT FROM KhachHang
            WHERE TenKH LIKE %s OR SDT LIKE %s OR MaKH LIKE %s
        """, (f"%{kw}%", f"%{kw}%", f"%{kw}%"))
        rows = cursor.fetchall()
        if rows:
            cb_kh['values'] = [f"{r[0]} - {r[1]} ({r[2]})" for r in rows]
            cb_kh.current(0)

    def add_customer_and_reload():
        open_kh_form(win, conn)
        load_customers()

    def clear_form():
        for k, v in entries.items():
            if k == "MaKH":
                cb_kh.set("")
                continue
            if k == "TongTien":
                tongtien_var.set("")
                continue
            try:
                v.config(state="normal")
            except:
                pass
            if hasattr(v, "delete"):
                v.delete(0, tk.END)
            if k == "MaHD":
                v.config(state="readonly")
        next_mahd()

    def load_data(search=None):
        tree.delete(*tree.get_children())
        temp_data.clear()

        query = """
            SELECT hd.MaHD, kh.TenKH, nv.HoTen, hd.TongTien, hd.NgayBan
            FROM HoaDon hd
            JOIN KhachHang kh ON hd.MaKH = kh.MaKH
            JOIN NhanVien nv ON hd.MaNV = nv.MaNV
        """

        if search:
            like = f"%{search}%"
            query += " WHERE kh.TenKH LIKE %s OR nv.HoTen LIKE %s"
            cursor.execute(query + " ORDER BY hd.MaHD ASC", (like, like))
        else:
            cursor.execute(query + " ORDER BY hd.MaHD ASC")

        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        next_mahd()
        load_customers()

    def add_temp():
        vals = {}
        vals["NgayBan"] = entries["NgayBan"].get().strip()

        mk = entries["MaKH"].get()
        vals["MaKH"] = mk.split(" - ")[0] if " - " in mk else mk.strip()

        vals["MaNV"] = getattr(root, "current_user_id", None) or entries["MaNV"].get().strip()
        vals["TongTien"] = "0"
        vals["GhiChu"] = entries["GhiChu"].get().strip()

        if not vals["NgayBan"] or not vals["MaKH"] or not vals["MaNV"]:
            messagebox.showwarning("Chú ý", "Vui lòng nhập đủ thông tin!")
            return

        temp_data.append(vals)
        messagebox.showinfo("Tạm", "Đã thêm hóa đơn.")
        clear_form()

    def save_all():
        if not temp_data:
            return messagebox.showinfo("Thông báo", "Không có dữ liệu để lưu.")

        try:
            for hd in temp_data:
                cursor.execute("""
                    INSERT INTO HoaDon (NgayBan, MaKH, MaNV, TongTien, GhiChu)
                    VALUES (%s,%s,%s,%s,%s)
                """, (hd["NgayBan"], hd["MaKH"], hd["MaNV"], hd["TongTien"], hd["GhiChu"]))
                conn.commit()

                cursor.execute("""
                    SELECT MaHD FROM HoaDon
                    WHERE NgayBan=%s AND MaKH=%s AND MaNV=%s
                    ORDER BY CreatedAt DESC LIMIT 1
                """, (hd["NgayBan"], hd["MaKH"], hd["MaNV"]))
                new_mahd = cursor.fetchone()[0]

                open_cthd_form(win, conn, new_mahd)

            temp_data.clear()
            load_data()
            messagebox.showinfo("OK", "Đã lưu!")

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", str(e))

    def delete_all():
        sel = tree.selection()
        if not sel:
            return
        mahd = tree.item(sel[0])['values'][0]

        if not messagebox.askyesno("Xác nhận", f"Xóa HĐ {mahd}?"):
            return

        cursor.execute("DELETE FROM HoaDon WHERE MaHD=%s", (mahd,))
        conn.commit()
        tree.delete(sel[0])
        clear_form()

    def open_selected_cthd():
        sel = tree.selection()
        if not sel:
            return
        mahd = tree.item(sel[0])['values'][0]
        open_cthd_form(win, conn, mahd)

    def on_select(event):
        sel = tree.selection()
        if not sel:
            return

        mahd, tenkh, tennv, tong, ngayban = tree.item(sel[0])['values']

        entries["MaHD"].config(state="normal")
        entries["MaHD"].delete(0, tk.END)
        entries["MaHD"].insert(0, mahd)
        entries["MaHD"].config(state="readonly")

        entries["NgayBan"].delete(0, tk.END)
        entries["NgayBan"].insert(0, ngayban)

        tongtien_var.set(tong)

    tree.bind("<<TreeviewSelect>>", on_select)

    # ===== NÚT CHỨC NĂNG =====
    btn_frame = tk.Frame(win, bg="#AEEBFF")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Thêm tạm", width=12,
              bg="#2196F3", fg="black",
              command=add_temp).grid(row=0, column=0, padx=6)

    tk.Button(btn_frame, text="Lưu", width=12,
              bg="#4CAF50", fg="black",
              command=save_all).grid(row=0, column=1, padx=6)

    tk.Button(btn_frame, text="Xóa", width=12,
              bg="#f44336", fg="black",
              command=delete_all).grid(row=0, column=2, padx=6)

    tk.Button(btn_frame, text="Mở chi tiết HĐ", width=14,
              bg="#2196F3", fg="black",
              command=open_selected_cthd).grid(row=0, column=3, padx=6)

    tk.Button(btn_frame, text="Hủy", width=12,
              bg="#9E9E9E", fg="black",
              command=clear_form).grid(row=0, column=4, padx=6)

    tk.Button(btn_frame, text="Quay lại", width=12,
              bg="#2196F3", fg="black",
              command=lambda: on_back()).grid(row=0, column=5, padx=6)
    def on_back():
        win.destroy()
        if is_standalone:
            root.destroy()
        else:
            root.deiconify()
    load_data()
    if is_standalone:
        win.mainloop()
if __name__ == "__main__":
    open_hd_form()
