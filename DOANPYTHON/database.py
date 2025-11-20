import mysql.connector
from mysql.connector import Error
def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ngoclinh1707@',
            database='QLCuaHangXeMay'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("❌ Lỗi kết nối MySQL:", e)
        return None
def close_connection(conn):
    """
    Đóng kết nối nếu nó đang mở. 
    Hàm này đã được thêm vào để khắc phục lỗi Import
    """
    if conn and conn.is_connected():
        conn.close()
def connect_and_get_cursor():
    """
    Hàm hỗ trợ: Kết nối database và trả về (kết nối, cursor).
    Dùng cho các form con cần thao tác CSDL.
    """
    conn = get_connection()
    if conn:
        # Sử dụng dictionary=True để cursor trả về dữ liệu dưới dạng dictionary (có tên cột)
        cursor = conn.cursor(dictionary=True) 
        return conn, cursor
    return None, None