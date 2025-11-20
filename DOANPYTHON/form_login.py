import tkinter as tk
from tkinter import ttk, messagebox
# Cần đảm bảo file database.py có hàm get_connection() và close_connection()
from database import get_connection, close_connection 
# Hàm được main.py gọi để mở cửa sổ đăng nhập. 
# Tham số root_app là cửa sổ chính của ứng dụng.
def open_login_form(root_app): 
    # Sử dụng root_app để tạo cửa sổ con (Toplevel)
    login_win = tk.Toplevel(root_app) 
    login_win.title("Đăng nhập hệ thống")
    login_win.geometry("400x350")
    login_win.resizable(False, False) 
    login_win.configure(bg="#B3E5FC")
    # RẤT QUAN TRỌNG: Bắt sự kiện đóng cửa sổ. Nếu đóng login, phải đóng luôn app.
    login_win.protocol("WM_DELETE_WINDOW", root_app.destroy) 
    login_win.grab_set() # Buộc người dùng tương tác với cửa sổ này
    # ==== TIÊU ĐỀ (Giữ nguyên giao diện ) ====
    lbl_title = tk.Label(
        login_win,
        text="ĐĂNG NHẬP",
        font=("Arial", 22, "bold"),
        bg="#B3E5FC",
        fg="#0D47A1"
    )
    lbl_title.pack(pady=20)
    # ==== FORM FRAME ====
    frm = tk.Frame(login_win, bg="#B3E5FC")
    frm.pack(pady=10)
    # --- Tài khoản ---
    tk.Label(frm, text="Tài khoản:", bg="#B3E5FC", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
    entry_user = tk.Entry(frm, width=30)
    entry_user.grid(row=1, column=0, pady=5)
    # entry_user.insert(0, "admin") #
    # --- Mật khẩu ---
    tk.Label(frm, text="Mật khẩu:", bg="#B3E5FC", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
    entry_pass = tk.Entry(frm, width=30, show="*")
    entry_pass.grid(row=3, column=0, pady=5)
    # entry_pass.insert(0, "0909") 
    # ==== CHECK LOGIN  ====
    def check_login():
        user = entry_user.get().strip()
        password = entry_pass.get().strip()

        if user == "" or password == "":
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ Tài khoản và Mật khẩu.")
            return
        
        conn = get_connection()
        if not conn: return
        
        cursor = None
        try:
            # SỬA LỖI LẤY DỮ LIỆU: Phải dùng dictionary=True để dễ lấy cột 'role'
            cursor = conn.cursor(dictionary=True) 
            cursor.execute("SELECT role FROM TaiKhoan WHERE username=%s AND password=%s", (user, password))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("Thành công", f"Đăng nhập thành công! Vai trò: {result['role']}")
                
                # 1. Lưu vai trò
                root_app.role = result['role'] 
                
                # 2. Đóng cửa sổ login
                login_win.destroy()
                
                ### PHẦN SỬA LỖI HIỂN THỊ ###
                root_app.deiconify() # HIỆN LẠI CỬA SỔ CHÍNH ĐÃ BỊ ẨN
                root_app.lift()      # Đưa cửa sổ lên trên cùng
                root_app.focus_force() # Buộc cửa sổ lấy focus
                
                # 3. Áp dụng quyền
                if hasattr(root_app, 'apply_role_permissions'):
                    root_app.apply_role_permissions()
                ### KẾT THÚC PHẦN SỬA LỖI ###
                
            else:
                messagebox.showerror("Sai thông tin", "Tài khoản hoặc mật khẩu không đúng.")
                
        except Exception as e:
             messagebox.showerror("Lỗi CSDL", f"Lỗi khi kiểm tra đăng nhập: {e}")
        finally:
            if cursor:
                cursor.close()
            close_connection(conn) # Đảm bảo đóng kết nối


    # ==== NÚT ĐĂNG NHẬP (Giữ nguyên giao diện của bạn) ====
    btn_login = tk.Button(
        login_win,
        text="Đăng nhập",
        width=15,
        height=2,
        bg="#64B5F6", 
        fg="black",
        command=check_login
    )
    btn_login.pack(pady=15)

    # Enter = Đăng nhập
    login_win.bind("<Return>", lambda e: check_login())

    # Chờ cửa sổ login đóng lại trước khi mainloop tiếp tục
    root_app.wait_window(login_win)