import tkinter as tk
from tkinter import ttk, messagebox

def open_lichsu_form(root=None, conn=None):
    cursor = conn.cursor()
    win = tk.Toplevel(root) if root else tk.Tk()
    win.title("Lịch sử thay đổi giá xe")
    win.geometry("900x520")
    win.configure(bg="#AEEBFF")   # 🌟 Nền xanh pastel

    # ====== TIÊU ĐỀ ======
    tk.Label(
        win,
        text="LỊCH SỬ THAY ĐỔI GIÁ XE",
        font=("Arial", 18, "bold"),
        fg="#003399",
        bg="#AEEBFF"
    ).pack(pady=10)

    # ====== FRAME SEARCH ======
    frame_search = tk.Frame(win, bg="#AEEBFF")
    frame_search.pack(pady=5)

    tk.Label(
        frame_search,
        text="Tìm theo Mã Xe hoặc Tên Xe:",
        font=("Arial", 11, "bold"),
        bg="#AEEBFF"
    ).grid(row=0, column=0)

    search_var = tk.StringVar()
    tk.Entry(frame_search, textvariable=search_var, width=40).grid(row=0, column=1, padx=5)

    # ====== LOAD DATA ======
    def load_data(search=None):
        tree.delete(*tree.get_children())

        if search:
            like = f"%{search}%"
            cursor.execute("""
                SELECT ls.ID, ls.MaXe, xm.TenXe,
                       ls.GiaCu, ls.GiaMoi, ls.NgayThayDoi
                FROM LichSuGiaXe ls
                JOIN XeMay xm ON ls.MaXe = xm.MaXe
                WHERE ls.MaXe LIKE %s OR xm.TenXe LIKE %s
                ORDER BY ls.ID DESC
            """, (like, like))
        else:
            cursor.execute("""
                SELECT ls.ID, ls.MaXe, xm.TenXe,
                       ls.GiaCu, ls.GiaMoi, ls.NgayThayDoi
                FROM LichSuGiaXe ls
                JOIN XeMay xm ON ls.MaXe = xm.MaXe
                ORDER BY ls.ID DESC
            """)

        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

    # ====== BUTTON SEARCH ======
    tk.Button(
        frame_search,
        text="Tìm",
        bg="#2196F3",
        fg="white",
        width=10,
        command=lambda: load_data(search_var.get())
    ).grid(row=0, column=2, padx=5)

    tk.Button(
        frame_search,
        text="Tải lại",
        bg="#9E9E9E",
        fg="white",
        width=10,
        command=lambda: (search_var.set(""), load_data())
    ).grid(row=0, column=3, padx=5)

    # ====== TABLE ======
    columns = ["ID", "MaXe", "TenXe", "GiaCu", "GiaMoi", "NgayThayDoi"]
    tree = ttk.Treeview(win, columns=columns, show="headings", height=10)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=140)

    tree.pack(padx=19, pady=10)

    # ====== LOAD FIRST TIME ======
    load_data()

    # ====== CHUẨN FORM CON ======
    if root:
        win.transient(root)   # nổi trên form cha
        win.grab_set()        # khóa focus form cha

    # KHÔNG dùng win.mainloop() khi là form con
    if not root:
        win.mainloop()


if __name__ == "__main__":
    from database import get_connection
    conn = get_connection()
    open_lichsu_form(None, conn)
