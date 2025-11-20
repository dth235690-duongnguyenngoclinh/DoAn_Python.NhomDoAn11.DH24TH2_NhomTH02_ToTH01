import tkinter as tk
from tkinter import ttk, messagebox
from form_LichSuGia import open_lichsu_form

# ===================== STYLE BUTTON  =====================
def style_button(btn, bg="#2196F3", fg="white"):
    btn.config(bg=bg,fg=fg,activebackground=bg, activeforeground=fg,relief="flat",bd=1)
def open_xe_form(root=None, conn=None):
    cursor = conn.cursor() if conn else None

    if root is not None:
        root.withdraw()

    win = tk.Toplevel(root) if root else tk.Tk()
    win.title("Quản lý Xe máy")
    win.geometry("1100x650")
    win.configure(bg="#AEEBFF") 
    # =================== TIÊU ĐỀ ===================
    tk.Label(
        win, text="QUẢN LÝ XE MÁY",font=("Arial", 20, "bold"),fg="#003399", bg="#AEEBFF").pack(pady=10)
    temp_data = []

        # =================== TÌM KIẾM ===================#
    search_frame = tk.Frame(win, bg="#AEEBFF")
    search_frame.pack(pady=5)

    tk.Label(search_frame, text="🔍 Tìm kiếm:", font=("Arial", 10, "bold"),bg="#AEEBFF").grid(row=0, column=0, padx=5)

    search_var = tk.StringVar()
    tk.Entry(search_frame, textvariable=search_var, width=60).grid(row=0, column=1, padx=5)
    # ---- NÚT TÌM  ----
    tk.Button(search_frame, text="Tìm", width=10, bg="#2196F3", fg="black", command=lambda: load_data(search_var.get())).grid(row=0, column=2, padx=5)
    # ---- NÚT TẢI LẠI  ----
    tk.Button(search_frame, text="Tải lại", width=10,bg="#9E9E9E", fg="black",command=lambda: (search_var.set(""), load_data())).grid(row=0, column=3, padx=5)
    # =================== BẢNG XE ===================
    frame_ds = tk.LabelFrame( win, text="Danh sách xe máy", padx=10, pady=10, font=("Arial", 11, "bold"), fg="#003366", bg="#AEEBFF")
    frame_ds.pack(padx=10, pady=10, fill="both", expand=True)

    scroll = tk.Scrollbar(frame_ds)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    columns = ["MaXe", "TenXe", "HangXe", "MauXe", "GiaXe", "SoLuong", "CreatedAt"]
    tree = ttk.Treeview(frame_ds, columns=columns, show="headings", yscrollcommand=scroll.set, height=12)
    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=150)
    tree.pack(fill="both", expand=True)
    scroll.config(command=tree.yview)
    # =================== FORM XE ===================
    frame_form = tk.LabelFrame( win, text="Thông tin xe máy",padx=10, pady=10, font=("Arial", 10, "bold"),bg="#AEEBFF")
    frame_form.pack(pady=10, padx=10, fill="x")
    entries = {}
    fields = ["MaXe", "TenXe", "HangXe", "MauXe", "GiaXe", "SoLuong"]
    for i, f in enumerate(fields):
        tk.Label(frame_form, text=f + ":", font=("Arial", 10), bg="#AEEBFF").grid(row=i // 3, column=(i % 3) * 2, sticky="w", padx=6, pady=4)
        e = tk.Entry(frame_form, width=25)
        e.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=6, pady=4)
        entries[f] = e
    # ====== MaXe readonly ======
    def set_auto_maxe():
        entries["MaXe"].config(state="normal")
        entries["MaXe"].delete(0, tk.END)
        entries["MaXe"].insert(0, "Auto (DB)")
        entries["MaXe"].config(state="readonly")
    set_auto_maxe()
    # =================== CLEAR FORM ===================
    def clear_form():
        for c in entries:
            entries[c].config(state="normal")
            entries[c].delete(0, tk.END)
        set_auto_maxe()
    # =================== LOAD DATA ===================
    def load_data(search=None):
        tree.delete(*tree.get_children())
        temp_data.clear()
        try:
            if search:
                like = f"%{search}%"
                cursor.execute("""
                    SELECT MaXe, TenXe, HangXe, MauXe, GiaXe, SoLuong, CreatedAt
                    FROM XeMay
                    WHERE MaXe LIKE %s OR TenXe LIKE %s OR HangXe LIKE %s OR MauXe LIKE %s
                       OR CAST(GiaXe AS CHAR) LIKE %s OR CAST(SoLuong AS CHAR) LIKE %s
                """, (like, like, like, like, like, like))
            else:
                cursor.execute("""
                    SELECT MaXe, TenXe, HangXe, MauXe, GiaXe, SoLuong, CreatedAt
                    FROM XeMay ORDER BY MaXe ASC
                """)
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)
            clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải dữ liệu: {e}")
    # =================== THÊM TẠM ===================
    def add_temp():
        vals = {
            "MaXe": "",
            "TenXe": entries["TenXe"].get().strip(),
            "HangXe": entries["HangXe"].get().strip(),
            "MauXe": entries["MauXe"].get().strip(),
            "GiaXe": entries["GiaXe"].get().strip(),
            "SoLuong": entries["SoLuong"].get().strip()
        }
        if not vals["TenXe"]:
            messagebox.showwarning("Thiếu", "Tên xe không được để trống!")
            return
        temp_data.append(vals)
        tree.insert("", tk.END,
                    values=["", vals["TenXe"], vals["HangXe"], vals["MauXe"], vals["GiaXe"], vals["SoLuong"], ""])
        clear_form()
    # =================== CẬP NHẬT XE ===================
    def update_xe():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chọn dòng", "Chọn xe cần cập nhật!")
            return

        maxe = entries["MaXe"].get()
        if maxe == "Auto (DB)":
            messagebox.showwarning("Lỗi", "Không thể cập nhật bản ghi chưa có trong DB!")
            return

        try:
            # Lấy giá cũ
            cursor.execute("SELECT GiaXe FROM XeMay WHERE MaXe=%s", (maxe,))
            old_price = cursor.fetchone()
            old_price = old_price[0] if old_price else None

            new_price = entries["GiaXe"].get()

            # Lưu lịch sử nếu giá thay đổi
            if str(old_price) != str(new_price):
                cursor.execute("""
                    INSERT INTO LichSuGiaXe (MaXe, GiaCu, GiaMoi, NgayThayDoi)
                    VALUES (%s, %s, %s, NOW())
                """, (maxe, old_price, new_price))

            # Cập nhật xe
            cursor.execute("""
                UPDATE XeMay 
                SET TenXe=%s, HangXe=%s, MauXe=%s, GiaXe=%s, SoLuong=%s
                WHERE MaXe=%s
            """, (
                entries["TenXe"].get(),
                entries["HangXe"].get(),
                entries["MauXe"].get(),
                entries["GiaXe"].get(),
                entries["SoLuong"].get(),
                maxe
            ))

            conn.commit()
            messagebox.showinfo("Thành công", f"Xe {maxe} đã được cập nhật!")
            load_data()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi cập nhật: {e}")

    # =================== LƯU DB ===================
    def save_all():
        if not temp_data:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để lưu.")
            return
        try:
            for xe in temp_data:
                cursor.execute("""
                    INSERT INTO XeMay (TenXe, HangXe, MauXe, GiaXe, SoLuong)
                    VALUES (%s,%s,%s,%s,%s)
                """, (xe["TenXe"], xe["HangXe"], xe["MauXe"], xe["GiaXe"], xe["SoLuong"]))

            conn.commit()
            temp_data.clear()
            load_data()
            messagebox.showinfo("OK", "Đã lưu xe mới!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi lưu: {e}")
    # =================== XÓA XE ===================
    def delete_xe():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chọn dòng", "Chọn xe cần xóa!")
            return
        maxe = tree.item(sel[0])["values"][0]
        if not messagebox.askyesno("Xác nhận", f"Xóa xe mã {maxe}?"):
            return
        try:
            cursor.execute("DELETE FROM XeMay WHERE MaXe=%s", (maxe,))
            conn.commit()
        except:
            pass
        tree.delete(sel[0])
        clear_form()
    # =================== CHỌN DÒNG ===================
    def on_select(event):
        sel = tree.selection()
        if not sel:
            return
        vals = tree.item(sel[0])["values"]
        for i, c in enumerate(columns[:-1]):
            entries[c].config(state="normal")
            entries[c].delete(0, tk.END)
            entries[c].insert(0, vals[i])
            if c == "MaXe":
                entries[c].config(state="readonly")
    tree.bind("<<TreeviewSelect>>", on_select)
    # =================== NÚT CHỨC NĂNG ===================
    frame_btn = tk.Frame(win, bg="#AEEBFF")
    frame_btn.pack(pady=10)

    tk.Button(frame_btn, text="Thêm tạm", width=12, command=add_temp,bg="#2196F3", fg="black").grid(row=0, column=0, padx=6)
    tk.Button(frame_btn, text="Lưu", width=12, command=save_all,bg="#4CAF50", fg="black").grid(row=0, column=1, padx=6)
    tk.Button(frame_btn, text="Cập nhật", width=12, command=update_xe,bg="#FFC107",fg="black").grid(row=0, column=2, padx=6)
    tk.Button(frame_btn, text="Xóa", width=12, command=delete_xe, bg="#f44336", fg="black").grid(row=0, column=3, padx=6)
    tk.Button(frame_btn, text="Hủy", width=12, command=clear_form,bg="#9E9E9E", fg="black").grid(row=0, column=4, padx=6)
    tk.Button(
    frame_btn, text="Lịch sử giá", width=12,
    command=lambda: open_lichsu_form(win, conn),
    bg="#00BCD4"
).grid(row=0, column=6, padx=6)


    def on_back():
        win.destroy()
        if root:
            root.deiconify()
    tk.Button(frame_btn, text="Quay lại", width=12, command=on_back,bg="#2196F3", fg="black").grid(row=0, column=5, padx=6)
    win.protocol("WM_DELETE_WINDOW", on_back)
    load_data()
# === Chạy riêng ===
if __name__ == "__main__":
    from database import get_connection
    conn = get_connection()
    open_xe_form(None, conn)
    tk.mainloop()
