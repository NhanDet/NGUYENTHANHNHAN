import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Quản Lý Sinh Viên")
        self.root.geometry("1000x700")
        self.conn = None
        self.cur = None

        # Tạo style cho giao diện
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Helvetica", 12), background="#f5f5f5")
        self.style.configure("TButton", font=("Helvetica", 12, 'bold'), padding=5)
        self.style.configure("TEntry", font=("Helvetica", 12))

        self.create_login_ui()

    def create_login_ui(self):
        """Giao diện đăng nhập"""
        self.login_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.login_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(self.login_frame, text="Đăng Nhập", font=("Helvetica", 24, 'bold'), bg="#f5f5f5").pack(pady=20)
        ttk.Label(self.login_frame, text="Tên đăng nhập:").pack(pady=5)
        self.username_entry = ttk.Entry(self.login_frame, width=30)
        self.username_entry.pack()

        ttk.Label(self.login_frame, text="Mật khẩu:").pack(pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*", width=30)
        self.password_entry.pack()

        login_btn = ttk.Button(self.login_frame, text="Đăng nhập", command=self.connect_db)
        login_btn.pack(pady=20)

    def connect_db(self):
        """Kết nối tới cơ sở dữ liệu"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        try:
            self.conn = psycopg2.connect(
                dbname='dbtest',
                user=username,
                password=password,
                host='localhost',
                port='5432'
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Thành công", "Kết nối thành công!")
            self.login_frame.destroy()
            self.create_main_ui()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối: {e}")

    def create_main_ui(self):
        """Tạo giao diện chính"""
        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(expand=1, fill='both')

        self.add_tab = ttk.Frame(self.tab_control, padding=20)
        self.view_tab = ttk.Frame(self.tab_control, padding=20)

        self.tab_control.add(self.add_tab, text='Thêm Sinh Viên')
        self.tab_control.add(self.view_tab, text='Danh Sách Sinh Viên')

        self.create_add_tab()
        self.create_view_tab()

    def create_add_tab(self):
        """Tab thêm sinh viên"""
        form_frame = tk.Frame(self.add_tab)
        form_frame.place(relx=0.5, rely=0.3, anchor='center')

        ttk.Label(form_frame, text="MSSV:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.mssv_entry = ttk.Entry(form_frame, width=30)
        self.mssv_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="Họ và Tên:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.hoten_entry = ttk.Entry(form_frame, width=30)
        self.hoten_entry.grid(row=1, column=1)

        ttk.Label(form_frame, text="Ngày sinh (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.ngaysinh_entry = ttk.Entry(form_frame, width=30)
        self.ngaysinh_entry.grid(row=2, column=1)

        ttk.Label(form_frame, text="Lớp:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.lop_entry = ttk.Entry(form_frame, width=30)
        self.lop_entry.grid(row=3, column=1)

        ttk.Button(form_frame, text="Thêm Sinh Viên", command=self.insert_data).grid(row=4, columnspan=2, pady=20)

    def insert_data(self):
        """Thêm sinh viên vào cơ sở dữ liệu"""
        mssv = self.mssv_entry.get().strip()
        hoten = self.hoten_entry.get().strip()
        ngaysinh = self.ngaysinh_entry.get().strip()
        lop = self.lop_entry.get().strip()

        if not mssv or not hoten or not ngaysinh or not lop:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            self.cur.execute(
                "INSERT INTO sinhvien (mssv, hoten, ngaysinh, lop) VALUES (%s, %s, %s, %s)",
                (mssv, hoten, ngaysinh, lop)
            )
            self.conn.commit()
            messagebox.showinfo("Thành công", "Thêm sinh viên thành công!")
            self.load_data()
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi thêm dữ liệu: {e}")

    def create_view_tab(self):
        """Tab xem danh sách sinh viên"""
        search_frame = tk.Frame(self.view_tab)
        search_frame.pack(anchor='w', pady=10)

        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=0, padx=10)
        ttk.Button(search_frame, text="Tìm kiếm", command=self.search_student).grid(row=0, column=1)

        self.tree = ttk.Treeview(self.view_tab, columns=('STT', 'MSSV', 'Họ và Tên', 'Ngày sinh', 'Lớp'), show='headings')
        self.tree.heading('STT', text='STT')
        self.tree.heading('MSSV', text='MSSV')
        self.tree.heading('Họ và Tên', text='Họ và Tên')
        self.tree.heading('Ngày sinh', text='Ngày sinh')
        self.tree.heading('Lớp', text='Lớp')
        self.tree.pack(fill='both', expand=True, pady=20)

        # Nút chức năng
        button_frame = tk.Frame(self.view_tab)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Load danh sách", command=self.load_data).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Xóa Sinh Viên", command=self.delete_student).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Chỉnh sửa", command=self.edit_student).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Sắp xếp theo Tên", command=self.sort_by_name).pack(side='left', padx=5)

    def load_data(self):
        """Load danh sách sinh viên"""
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("SELECT mssv, hoten, ngaysinh, lop FROM sinhvien ORDER BY mssv")
        rows = self.cur.fetchall()
        for index, row in enumerate(rows, start=1):
            self.tree.insert("", "end", values=(index, *row))

    def search_student(self):
        """Tìm kiếm sinh viên"""
        search_term = self.search_entry.get().strip()
        self.cur.execute("SELECT * FROM sinhvien WHERE mssv LIKE %s OR hoten LIKE %s ORDER BY mssv", (f"%{search_term}%", f"%{search_term}%"))
        rows = self.cur.fetchall()
        self.tree.delete(*self.tree.get_children())
        for index, row in enumerate(rows, start=1):
            self.tree.insert("", "end", values=(index, *row))

    def delete_student(self):
        """Xóa sinh viên"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên để xóa!")
            return

        mssv = str(self.tree.item(selected_item)['values'][1])
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa sinh viên với MSSV: {mssv}?")
        if not confirm:
            return

        try:
            self.cur.execute("DELETE FROM sinhvien WHERE mssv = %s", (mssv,))
            self.conn.commit()
            messagebox.showinfo("Thành công", "Xóa sinh viên thành công!")
            self.load_data()
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi xóa sinh viên: {e}")

    def edit_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên để chỉnh sửa!")
            return

        # Lấy thông tin sinh viên từ bảng
        mssv = str(self.tree.item(selected_item)['values'][1])  # MSSV
        hoten = str(self.tree.item(selected_item)['values'][2])
        ngaysinh = str(self.tree.item(selected_item)['values'][3])
        lop = str(self.tree.item(selected_item)['values'][4])

        # Tạo cửa sổ chỉnh sửa
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Chỉnh sửa thông tin sinh viên")
        edit_window.geometry("400x300")

        form_frame = tk.Frame(edit_window)
        form_frame.place(relx=0.5, rely=0.3, anchor='center')

        # Thêm trường MSSV cho phép chỉnh sửa
        ttk.Label(form_frame, text="MSSV:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.mssv_entry = ttk.Entry(form_frame, width=30)
        self.mssv_entry.grid(row=0, column=1)
        self.mssv_entry.insert(0, mssv)  # Hiển thị MSSV để chỉnh sửa

        # Các trường khác
        ttk.Label(form_frame, text="Họ và Tên:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.hoten_entry = ttk.Entry(form_frame, width=30)
        self.hoten_entry.grid(row=1, column=1)
        self.hoten_entry.insert(0, hoten)

        ttk.Label(form_frame, text="Ngày sinh (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.ngaysinh_entry = ttk.Entry(form_frame, width=30)
        self.ngaysinh_entry.grid(row=2, column=1)
        self.ngaysinh_entry.insert(0, ngaysinh)

        ttk.Label(form_frame, text="Lớp:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.lop_entry = ttk.Entry(form_frame, width=30)
        self.lop_entry.grid(row=3, column=1)
        self.lop_entry.insert(0, lop)

        # Nút để lưu thay đổi
        ttk.Button(form_frame, text="Lưu Thay Đổi", command=lambda: self.update_student(edit_window)).grid(row=4, columnspan=2, pady=20)

    def update_student(self, edit_window):
        mssv = self.mssv_entry.get().strip()  # Lấy MSSV từ trường nhập liệu
        hoten = self.hoten_entry.get().strip()
        ngaysinh = self.ngaysinh_entry.get().strip()
        lop = self.lop_entry.get().strip()

        if not mssv or not hoten or not ngaysinh or not lop:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            self.cur.execute(
                "UPDATE sinhvien SET mssv = %s, hoten = %s, ngaysinh = %s, lop = %s WHERE mssv = %s",
                (mssv, hoten, ngaysinh, lop, mssv)  # Cập nhật MSSV
            )
            self.conn.commit()
            messagebox.showinfo("Thành công", "Cập nhật thông tin sinh viên thành công!")
            self.load_data()
            edit_window.destroy()
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật thông tin sinh viên: {e}")

    def sort_by_name(self):
        """Sắp xếp sinh viên theo họ và tên"""
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("SELECT mssv, hoten, ngaysinh, lop FROM sinhvien ORDER BY hoten")
        rows = self.cur.fetchall()
        for index, row in enumerate(rows, start=1):
            self.tree.insert("", "end", values=(index, *row))

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()