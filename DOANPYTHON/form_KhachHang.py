import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
def open_kh_form(root=None, conn=None):
    cursor = conn.cursor() if conn else None
    if root is not None:
        root.withdraw()
    win = tk.Toplevel(root) if root is not None else tk.Tk()
    win.title("Quản lý Khách hàng")
    win.geometry("1100x650")
    win.configure(bg="#AEEBFF")   # 🌟 Nền xanh giống form Xe/NV
    tk.Label(win, text="QUẢN LÝ KHÁCH HÀNG",font=("Arial", 20, "bold"),fg="#003399", bg="#AEEBFF").pack(pady=10)
    # ================= TÌM KIẾM =================
    frame_search = tk.Frame(win, bg="#AEEBFF")
    frame_search.pack(pady=5)
    tk.Label(frame_search, text="🔍 Tìm kiếm:", font=("Arial", 10, "bold"),bg="#AEEBFF").grid(row=0, column=0, padx=5)
    search_var = tk.StringVar()
    tk.Entry(frame_search, textvariable=search_var, width=60).grid(row=0, column=1, padx=5)
    tk.Button(frame_search, text="Tìm", bg="#2196F3", fg="black", width=10,command=lambda: load_data(search_var.get())).grid(row=0, column=2, padx=5)
    tk.Button(frame_search, text="Tải lại", bg="#9E9E9E", fg="black", width=10,command=lambda: (search_var.set(""), load_data())).grid(row=0, column=3, padx=5)
    # ================= BẢNG KHÁCH HÀNG =================
    frame_ds = tk.LabelFrame(win, text="Danh sách khách hàng",padx=10, pady=10,font=("Arial", 11, "bold"),fg="#003366", bg="#AEEBFF")
    frame_ds.pack(padx=10, pady=10, fill="both", expand=True)
    scroll = tk.Scrollbar(frame_ds)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    columns = ["MaKH", "TenKH", "DiaChi", "SDT", "Email"]
    tree = ttk.Treeview(frame_ds, columns=columns, show="headings", yscrollcommand=scroll.set, height=12)
    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=180)
    tree.pack(fill="both", expand=True)
    scroll.config(command=tree.yview)
    # ================= FORM NHẬP =================
    frame_form = tk.LabelFrame(
        win, text="Thông tin khách hàng",padx=10, pady=10,font=("Arial", 10, "bold"), bg="#AEEBFF")
    frame_form.pack(pady=10, padx=10, fill="x")
    entries = {}
    fields = ["MaKH", "TenKH", "DiaChi", "SDT", "Email"]
    for i, f in enumerate(fields):
        tk.Label(frame_form, text=f + ":", font=("Arial", 10),bg="#AEEBFF").grid(row=i // 3, column=(i % 3) * 2,sticky="w", padx=6, pady=4)
        e = tk.Entry(frame_form, width=25)
        e.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=6, pady=4)
        entries[f] = e
    # ====== MaKH readonly ======
    def set_auto_makh():
        entries["MaKH"].config(state="normal")
        entries["MaKH"].delete(0, tk.END)
        entries["MaKH"].insert(0, "Auto (DB)")
        entries["MaKH"].config(state="readonly")
    set_auto_makh()
    temp_data = []
    # =============== CLEAR FORM =================
    def clear_form():
        for c in entries:
            entries[c].config(state="normal")
            entries[c].delete(0, tk.END)
        set_auto_makh()
    # =============== LOAD DATA ==================
    def load_data(search=None):
        tree.delete(*tree.get_children())
        temp_data.clear()
        try:
            if search:
                like = f"%{search}%"
                cursor.execute("""
                    SELECT MaKH, TenKH, DiaChi, SDT, Email 
                    FROM KhachHang
                    WHERE MaKH LIKE %s OR TenKH LIKE %s 
                       OR DiaChi LIKE %s OR SDT LIKE %s OR Email LIKE %s
                """, (like, like, like, like, like))
            else:
                cursor.execute("SELECT MaKH, TenKH, DiaChi, SDT, Email FROM KhachHang ORDER BY MaKH ASC")

            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)
            clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải dữ liệu: {e}")
    # =============== THÊM TẠM ==================
    def add_temp():
        vals = {
            "MaKH": "",
            "TenKH": entries["TenKH"].get().strip(),
            "DiaChi": entries["DiaChi"].get().strip(),
            "SDT": entries["SDT"].get().strip(),
            "Email": entries["Email"].get().strip()
        }
        if not vals["TenKH"]:
            messagebox.showwarning("Thiếu", "Tên khách hàng không được để trống!")
            return
        temp_data.append(vals)
        tree.insert("", tk.END, values=["", vals["TenKH"], vals["DiaChi"], vals["SDT"], vals["Email"]])
        clear_form()
    # =============== CẬP NHẬT KH ==================
    def update_kh():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chọn dòng", "Chọn khách hàng cần cập nhật!")
            return
        makh = entries["MaKH"].get()
        if makh == "Auto (DB)":
            messagebox.showwarning("Lỗi", "Không thể cập nhật bản ghi chưa có trong database!")
            return
        try:
            cursor.execute("""
                UPDATE KhachHang 
                SET TenKH=%s, DiaChi=%s, SDT=%s, Email=%s
                WHERE MaKH=%s
            """, (
                entries["TenKH"].get(),
                entries["DiaChi"].get(),
                entries["SDT"].get(),
                entries["Email"].get(),
                makh
            ))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã cập nhật khách hàng {makh}!")
            load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi cập nhật: {e}")
    # =============== LƯU VÀO DB =================
    def save_all():
        if not temp_data:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để lưu.")
            return
        try:
            for kh in temp_data:
                cursor.execute("""
                    INSERT INTO KhachHang (TenKH, DiaChi, SDT, Email)
                    VALUES (%s,%s,%s,%s)
                """, (kh["TenKH"], kh["DiaChi"], kh["SDT"], kh["Email"]))
            conn.commit()
            temp_data.clear()
            load_data()
            messagebox.showinfo("OK", "Đã lưu khách hàng mới!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi lưu dữ liệu: {e}")
    # =============== XÓA KH =====================
    def delete_kh():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chọn dòng", "Chọn khách hàng để xóa!")
            return
        makh = tree.item(sel[0])["values"][0]
        if not messagebox.askyesno("Xác nhận", f"Xóa khách hàng {makh}?"):
            return
        try:
            cursor.execute("DELETE FROM KhachHang WHERE MaKH=%s", (makh,))
            conn.commit()
        except:
            pass
        tree.delete(sel[0])
        clear_form()
    # =============== CHỌN DÒNG ==================
    def on_select(event):
        sel = tree.selection()
        if not sel:
            return
        vals = tree.item(sel[0])["values"]
        for i, c in enumerate(columns):
            entries[c].config(state="normal")
            entries[c].delete(0, tk.END)
            entries[c].insert(0, vals[i])
            if c == "MaKH":
                entries[c].config(state="readonly")
    tree.bind("<<TreeviewSelect>>", on_select)
    # =============== NÚT CHỨC NĂNG ===============
    frame_btn = tk.Frame(win, bg="#AEEBFF")
    frame_btn.pack(pady=10)

    tk.Button(frame_btn, text="Thêm tạm", width=12, command=add_temp, bg="#2196F3", fg="black").grid(row=0, column=0, padx=6)
    tk.Button(frame_btn, text="Lưu", width=12, command=save_all,bg="#4CAF50", fg="black").grid(row=0, column=1, padx=6)
    tk.Button(frame_btn, text="Cập nhật", width=12, command=update_kh,bg="#FFC107", fg="black").grid(row=0, column=2, padx=6)
    tk.Button(frame_btn, text="Xóa", width=12, command=delete_kh,bg="#f44336", fg="black").grid(row=0, column=3, padx=6)
    tk.Button(frame_btn, text="Hủy", width=12, command=clear_form, bg="#9E9E9E", fg="black").grid(row=0, column=4, padx=6)
    def on_back():
        win.destroy()
        if root is not None:
            root.deiconify()
    tk.Button(frame_btn, text="Quay lại", width=12, command=on_back,bg="#2196F3", fg="black").grid(row=0, column=5, padx=6)
    win.protocol("WM_DELETE_WINDOW", on_back)
    load_data()
# === Chạy riêng ==
if __name__ == "__main__":
    conn = get_connection()
    open_kh_form(None, conn)
    tk.mainloop()
