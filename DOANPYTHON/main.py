import tkinter as tk
from tkinter import messagebox
from database import get_connection
# các form con
from form_XeMay import open_xe_form
from form_NhanVien import open_nv_form
from form_KhachHang import open_kh_form
from form_HoaDon import open_hd_form
from form_CTHoaDon import open_cthd_form
from form_login import open_login_form

# ===================== TẠO CANVAS BO GÓC =====================
def _create_round_rect(self, x1, y1, x2, y2, radius=15, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return self.create_polygon(points, smooth=True, **kwargs)
tk.Canvas.create_round_rect = _create_round_rect
# ===================== TẠO NÚT ĐẸP + HOVER =====================
def create_button(master, text, bg_color="#64B5F6", command=None):
    frame = tk.Frame(master, bg=master["bg"])
    frame.pack(pady=10)
    canvas = tk.Canvas(frame, width=300, height=50,
                        bg=master["bg"], highlightthickness=0)
    canvas.pack()
    rect = canvas.create_round_rect(2, 2, 298, 48, radius=12,
                                     fill=bg_color, outline="#1E88E5", width=2)
    lbl = tk.Label(canvas, text=text, font=("Arial", 12, "bold"),
                      bg=bg_color, fg="black")
    canvas.create_window(150, 25, window=lbl)
    # Hover effect
    def on_enter(e):
        canvas.itemconfig(rect, fill="#42A5F5")
        lbl.config(bg="#42A5F5")
    def on_leave(e):
        canvas.itemconfig(rect, fill=bg_color)
        lbl.config(bg=bg_color)
    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    lbl.bind("<Enter>", on_enter)
    lbl.bind("<Leave>", on_leave)
    if command:
        # Bắt sự kiện click vào Label
        lbl.bind("<Button-1>", lambda e: command())
        # Bắt sự kiện click vào Canvas (phòng trường hợp click vào viền)
        canvas.bind("<Button-1>", lambda e: command())
    return frame
# ===================== MAIN =====================
conn = get_connection()
if not conn:
    tk.messagebox.showerror("Lỗi", "Không kết nối được MySQL. Kiểm tra database.py")
    # Nếu không kết nối được DB, ứng dụng phải thoát ngay
    raise SystemExit("Không kết nối DB")
root = tk.Tk()
root.title("Quản Lý Cửa Hàng Xe Máy")
root.geometry("600x620")
root.configure(bg="#D6F4FF")
root.role = None # Biến lưu vai trò người dùng (Admin/Nhan_Vien)
# Ẩn menu chính để login trước
root.withdraw()
open_login_form(root)
# ===================== XỬ LÝ THOÁT ỨNG DỤNG =====================
def confirm_exit():
    # Sử dụng root.withdraw() để ẩn cửa sổ chính trong khi hỏi xác nhận, tránh lỗi focus
    root.withdraw() 
    if messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn thoát?"):
        try:
            # Đảm bảo kết nối database được đóng trước khi thoát
            if conn:
                conn.close()
        except Exception:
            # Bỏ qua lỗi nếu conn đã bị đóng rồi
            pass
        root.destroy()
    else:
        # Nếu người dùng chọn No, hiển thị lại cửa sổ chính
        root.deiconify() 
        root.lift()
        root.focus_force()
# DÒNG CODE QUAN TRỌNG ĐÃ THÊM/SỬA LỖI: Gắn hàm confirm_exit vào nút 'X'
root.protocol("WM_DELETE_WINDOW", confirm_exit)
# ===================== TIÊU ĐỀ =====================
tk.Label(root,
          text="QUẢN LÝ CỬA HÀNG",
          font=("Arial", 28, "bold"),
          fg="#0D47A1",
          bg="#D6F4FF"
          ).pack(pady=30)
# ===================== MENU CÁC NÚT =====================
# Truyền root và conn vào các form con
btn_xe = create_button(root, "QUẢN LÝ XE MÁY",command=lambda: open_xe_form(root, conn))
btn_nv = create_button(root, "QUẢN LÝ NHÂN VIÊN",command=lambda: open_nv_form(root, conn))
btn_kh = create_button(root, "QUẢN LÝ KHÁCH HÀNG",command=lambda: open_kh_form(root, conn))
btn_hd = create_button(root, "QUẢN LÝ HÓA ĐƠN",command=lambda: open_hd_form(root, conn))
btn_cthd = create_button(root, "QUẢN LÝ CHI TIẾT HÓA ĐƠN",command=lambda: open_cthd_form(root, conn))
# ===================== NÚT THOÁT =====================
create_button(root, "THOÁT", bg_color="#E57373",
              command=confirm_exit) # Đảm bảo nút này gọi hàm confirm_exit
# ===================== ẨN CHỨC NĂNG THEO QUYỀN =====================
def apply_role_permissions():
    # Nếu nhân viên → ẩn mục quản lý nhân viên
    if root.role == "Nhan_Vien":
        btn_nv.pack_forget()
    # Thêm các logic ẩn/hiện khác nếu cần
root.apply_role_permissions = apply_role_permissions
# ===================== RUN =====================
root.mainloop()