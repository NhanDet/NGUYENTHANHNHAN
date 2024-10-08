import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class QuanLyThoiGian:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý thời gian hằng ngày")
        self.root.geometry("400x400")
        self.root.config(bg="#f0f0f0")  # Màu nền dễ nhìn
        self.root.resizable(False, False)  # Khóa phóng to cửa sổ
        
        # Danh sách cảnh báo
        self.canhbao_list = []
        # Ngưỡng cảnh báo (phút)
        self.nguongcanhbao = {"Học Tập": 300, "Giải Trí": 240, "Làm Việc": 180}
        # Tổng thời gian
        self.total_time = 1440  # 1440 phút = 24 giờ
        # Nơi chứa giá trị vừa nhập
        self.recent_study = 0
        self.recent_entertainment = 0
        self.recent_work = 0

        # Giao diện
        self.giao_dien()
        self.thanh_menu()

    def nhap_data(self):
        try:
            study = float(self.entry_study.get())
            entertainment = float(self.entry_entertainment.get())
            work = float(self.entry_work.get())

            # Lưu các giá trị vừa nhập gần nhất
            self.recent_study = study
            self.recent_entertainment = entertainment
            self.recent_work = work

            # Kiểm tra nếu vượt quá thời gian cho từng hoạt động
            if study > self.nguongcanhbao["Học Tập"]:
                canhbao_message = "Thời gian dành cho Học Tập quá mức!"
                self.canhbao_list.append(canhbao_message)
                messagebox.showwarning("Cảnh báo", canhbao_message)
            if entertainment > self.nguongcanhbao["Giải Trí"]:
                canhbao_message = "Thời gian dành cho Giải Trí quá mức!"
                self.canhbao_list.append(canhbao_message)
                messagebox.showwarning("Cảnh báo", canhbao_message)
            if work > self.nguongcanhbao["Làm Việc"]:
                canhbao_message = "Thời gian dành cho Làm Việc quá mức!"
                self.canhbao_list.append(canhbao_message)
                messagebox.showwarning("Cảnh báo", canhbao_message)

            # Xóa các ô sau khi nhấn nút kiểm tra 
            self.entry_study.delete(0, tk.END)
            self.entry_entertainment.delete(0, tk.END)
            self.entry_work.delete(0, tk.END)

            messagebox.showinfo("Thông báo", "Dữ liệu được lưu thành công!")

        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập giá trị số hợp lệ và không để trống!")

    def show_thongso(self):
        hienthi2 = (f"Học Tập: {self.recent_study} phút\n"
                    f"Giải Trí: {self.recent_entertainment} phút\n"
                    f"Làm Việc: {self.recent_work} phút")
        messagebox.showinfo("Thông số thời gian", hienthi2)

    def show_tongthoigian(self):
        tong_thoigian = self.recent_study + self.recent_entertainment + self.recent_work
        if tong_thoigian > self.total_time:
            messagebox.showwarning("Cảnh báo", f"Tổng thời gian vượt quá 24 giờ!")
        else:
            messagebox.showinfo("Tổng thời gian", f"Tổng thời gian sử dụng: {tong_thoigian} phút")

    def giao_dien(self):
        frame_nhap = ttk.LabelFrame(self.root, text="Nhập thời gian cho các hoạt động", padding=(10, 5))
        frame_nhap.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Tạo Label trong frame nhập
        label_study = ttk.Label(frame_nhap, text="Học Tập (phút):")
        label_study.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_study = ttk.Entry(frame_nhap)
        self.entry_study.grid(row=0, column=1, padx=10, pady=5)
        self.entry_study.focus()

        label_entertainment = ttk.Label(frame_nhap, text="Giải Trí (phút):")
        label_entertainment.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_entertainment = ttk.Entry(frame_nhap)
        self.entry_entertainment.grid(row=1, column=1, padx=10, pady=5)

        label_work = ttk.Label(frame_nhap, text="Làm Việc (phút):")
        label_work.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_work = ttk.Entry(frame_nhap)
        self.entry_work.grid(row=2, column=1, padx=10, pady=5)

        # Button kiểm tra thời gian
        frame_ketqua = ttk.LabelFrame(self.root, text="Kiểm tra thời gian", padding=(10, 5))
        frame_ketqua.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky='w')

        submit_button = ttk.Button(frame_ketqua, text="Kiểm tra", command=self.nhap_data)
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def thanh_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Thêm menubar
        tongthoigian_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Tổng thời gian", menu=tongthoigian_menu)
        tongthoigian_menu.add_command(label="Hiển thị tổng thời gian", command=self.show_tongthoigian)

        thongso_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Thông số", menu=thongso_menu)
        thongso_menu.add_command(label="Hiển thị thông số", command=self.show_thongso)


if __name__ == "__main__":
    root = tk.Tk()  
    app = QuanLyThoiGian(root)  
    root.mainloop()
