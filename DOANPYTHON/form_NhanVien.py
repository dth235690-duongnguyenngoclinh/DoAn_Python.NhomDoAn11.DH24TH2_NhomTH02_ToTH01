import tkinter as tk
from tkinter import ttk, messagebox
def open_nv_form(root=None, conn=None):
    cursor = conn.cursor() if conn else None
    if root is not None:
        root.withdraw()
    win = tk.Toplevel(root) if root is not None else tk.Tk()
    win.title("Quản lý Nhân Viên")
    win.geometry("1100x650")
    win.configure(bg="#AEEBFF")
    # ===== TIÊU ĐỀ =====
    tk.Label( win,text="QUẢN LÝ NHÂN VIÊN",font=("Arial", 20, "bold"),fg="#003399",bg="#AEEBFF").pack(pady=10)
    temp_data = []
    # ===================== TÌM KIẾM =====================
    search_frame = tk.Frame(win, bg="#AEEBFF")
    search_frame.pack(pady=5)
    tk.Label(search_frame, text="🔍 Tìm kiếm:", font=("Arial", 11, "bold"), bg="#AEEBFF").grid(row=0, column=0, padx=5)
    search_var = tk.StringVar()
    tk.Entry(search_frame, textvariable=search_var, width=60).grid(row=0, column=1, padx=5)
    # ---- Nút Tìm ----
    tk.Button(search_frame, text="Tìm", width=10,bg="#2196F3", fg="black",command=lambda: load_data(search_var.get())).grid(row=0, column=2, padx=5)
    # ---- Nút Tải lại ----
    tk.Button(search_frame, text="Tải lại", width=10,bg="#9E9E9E", fg="black",command=lambda: (search_var.set(""), load_data())).grid(row=0, column=3, padx=5)
    # ===================== DANH SÁCH NHÂN VIÊN =====================
    frame_ds = tk.LabelFrame(
        win,
        text="Danh sách nhân viên",
        padx=10, pady=10,
        font=("Arial", 11, "bold"),
        fg="#003366",
        bg="#AEEBFF"
    )
    frame_ds.pack(padx=10, pady=10, fill="both", expand=True)
    scroll = tk.Scrollbar(frame_ds)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    columns = ["MaNV", "HoTen", "GioiTinh", "NgaySinh", "SDT", "DiaChi", "ChucVu", "Luong", "CreatedAt"]
    tree = ttk.Treeview(frame_ds, columns=columns, show="headings", yscrollcommand=scroll.set, height=12)
    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=130)
    tree.pack(fill="both", expand=True)
    scroll.config(command=tree.yview)
    # ===================== FORM NHẬP =====================
    form = tk.LabelFrame(
        win,
        text="Thông tin nhân viên",
        padx=10, pady=10,
        font=("Arial", 10, "bold"),
        bg="#AEEBFF"
    )
    form.pack(pady=10, padx=10, fill="x")
    entries = {}
    fields = ["MaNV", "HoTen", "GioiTinh", "NgaySinh", "SDT", "DiaChi", "ChucVu", "Luong"]
    for i, c in enumerate(fields):
        tk.Label(form, text=c + ":", font=("Arial", 10), bg="#AEEBFF").grid(
            row=i // 3, column=(i % 3) * 2, sticky="w", padx=6, pady=4
        )
        e = tk.Entry(form, width=25)
        e.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=6, pady=4)
        entries[c] = e
    # ===== AUTO MÃ NV =====
    def set_auto_manv():
        entries["MaNV"].config(state="normal")
        entries["MaNV"].delete(0, tk.END)
        entries["MaNV"].insert(0, "Auto (DB)")
        entries["MaNV"].config(state="readonly")
    set_auto_manv()
    # ===== CLEAR FORM =====
    def clear_form():
        for c in entries:
            entries[c].config(state="normal")
            entries[c].delete(0, tk.END)
        set_auto_manv()
    # ===================== LOAD DATA =====================
    def load_data(search=None):
        tree.delete(*tree.get_children())
        temp_data.clear()
        try:
            if search:
                like = f"%{search}%"
                cursor.execute("""
                    SELECT MaNV, HoTen, GioiTinh, NgaySinh, SDT, DiaChi, ChucVu, Luong, CreatedAt
                    FROM NhanVien
                    WHERE MaNV LIKE %s 
                       OR HoTen LIKE %s 
                       OR GioiTinh LIKE %s 
                       OR SDT LIKE %s
                       OR DiaChi LIKE %s
                       OR ChucVu LIKE %s
                """, (like, like, like, like, like, like))
            else:
                cursor.execute("""
                    SELECT MaNV, HoTen, GioiTinh, NgaySinh, SDT, DiaChi, ChucVu, Luong, CreatedAt
                    FROM NhanVien ORDER BY MaNV ASC
                """)
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)
            clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi load dữ liệu: {e}")
    # ===================== THÊM TẠM =====================
    def add_temp():
        vals = {c: entries[c].get().strip() for c in entries}
        if not vals["HoTen"]:
            messagebox.showwarning("Thiếu", "Họ tên không được để trống!")
            return
        temp_data.append(vals)
        tree.insert("", tk.END, values=[
            "", vals["HoTen"], vals["GioiTinh"], vals["NgaySinh"],
            vals["SDT"], vals["DiaChi"], vals["ChucVu"], vals["Luong"], ""
        ])
        clear_form()
    # ===================== CẬP NHẬT =====================
    def update_nv():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chú ý", "Chọn nhân viên cần cập nhật!")
            return
        manv = entries["MaNV"].get()
        if manv == "Auto (DB)":
            messagebox.showwarning("Lỗi", "Không thể cập nhật bản ghi chưa có trong DB!")
            return
        hoten = entries["HoTen"].get()
        gt = entries["GioiTinh"].get()
        ns = entries["NgaySinh"].get()
        sdt = entries["SDT"].get()
        dc = entries["DiaChi"].get()
        cv = entries["ChucVu"].get()
        luong = entries["Luong"].get()
        try:
            cursor.execute("""
                UPDATE NhanVien 
                SET HoTen=%s, GioiTinh=%s, NgaySinh=%s, SDT=%s, DiaChi=%s, ChucVu=%s, Luong=%s
                WHERE MaNV=%s
            """, (hoten, gt, ns, sdt, dc, cv, luong, manv))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã cập nhật nhân viên {manv}!")
            load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi cập nhật: {e}")
    # ===================== LƯU DB =====================
    def save_all():
        if not temp_data:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để lưu.")
            return
        try:
            for nv in temp_data:
                cursor.execute("""
                    INSERT INTO NhanVien (HoTen, GioiTinh, NgaySinh, SDT, DiaChi, ChucVu, Luong)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (nv["HoTen"], nv["GioiTinh"], nv["NgaySinh"],
                      nv["SDT"], nv["DiaChi"], nv["ChucVu"], nv["Luong"]))
            conn.commit()
            temp_data.clear()
            load_data()
            messagebox.showinfo("OK", "Đã lưu dữ liệu mới!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi lưu dữ liệu: {e}")
    # ===================== XÓA =====================
    def delete_nv():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chọn dòng", "Phải chọn nhân viên để xóa!")
            return

        manv = tree.item(sel[0])["values"][0]

        if not messagebox.askyesno("Xác nhận", f"Xóa nhân viên {manv}?"):
            return

        try:
            cursor.execute("DELETE FROM NhanVien WHERE MaNV=%s", (manv,))
            conn.commit()
        except:
            pass

        tree.delete(sel[0])
        clear_form()
    # ===================== CLICK BẢNG =====================
    def on_select(event):
        sel = tree.selection()
        if not sel:
            return
        vals = tree.item(sel[0])["values"]
        for i, c in enumerate(columns[:-1]):
            entries[c].config(state="normal")
            entries[c].delete(0, tk.END)
            entries[c].insert(0, vals[i])
            if c == "MaNV":
                entries[c].config(state="readonly")
    tree.bind("<<TreeviewSelect>>", on_select)
    # ===================== BUTTON BAR =====================
    btn_frame = tk.Frame(win, bg="#AEEBFF")
    btn_frame.pack(pady=10)
    # Thêm tạm
    tk.Button(btn_frame, text="Thêm tạm", width=12, command=add_temp,
              bg="#2196F3", fg="black").grid(row=0, column=0, padx=6)
    # Lưu
    tk.Button(btn_frame, text="Lưu", width=12, command=save_all,
              bg="#4CAF50", fg="black").grid(row=0, column=1, padx=6)
    # Cập nhật
    tk.Button(btn_frame, text="Cập nhật", width=12, command=update_nv,
              bg="#FFC107", fg="black").grid(row=0, column=2, padx=6)
    # Xóa
    tk.Button(btn_frame, text="Xóa", width=12, command=delete_nv,
              bg="#f44336", fg="black").grid(row=0, column=3, padx=6)
    # Hủy
    tk.Button(btn_frame, text="Hủy", width=12, command=clear_form,
              bg="#9E9E9E", fg="black").grid(row=0, column=4, padx=6)
    # Quay lại
    def on_back():
        win.destroy()
        if root is not None:
            root.deiconify()
    tk.Button(btn_frame, text="Quay lại", width=12, command=on_back,
              bg="#2196F3", fg="black").grid(row=0, column=5, padx=6)
    win.protocol("WM_DELETE_WINDOW", on_back)
    load_data()
# === Chạy riêng ===
if __name__ == "__main__":
    from database import get_connection
    conn = get_connection()
    open_nv_form(None, conn)
    tk.mainloop()
